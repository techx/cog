from hardwarecheckout import app
from hardwarecheckout.models import db

from hardwarecheckout.controllers.request import request_update

from hardwarecheckout.models.item import Item
from hardwarecheckout.models.inventory_entry import InventoryEntry
from hardwarecheckout.models.inventory_entry import ItemType
from hardwarecheckout.models.user import User
from hardwarecheckout.models.request import Request, RequestStatus

from hardwarecheckout.forms.inventory_form import InventoryForm
from hardwarecheckout.forms.inventory_update_form import InventoryUpdateForm
from hardwarecheckout.forms.inventory_import_form import InventoryImportForm

from hardwarecheckout.utils import requires_auth, requires_admin, auth_optional

from hardwarecheckout.sheets_csv import get_csv, SheetsImportError

from flask import jsonify
from werkzeug.datastructures import MultiDict

from sqlalchemy import func

import urllib2
import urlparse
import requests
from bs4 import BeautifulSoup

import random

import os

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template,
    jsonify,
    url_for
)

@app.route('/inventory')
@auth_optional()
def inventory():
    """Render inventory"""
    lottery_query = InventoryEntry.query.filter_by(
        item_type = ItemType.LOTTERY)
    checkout_query = InventoryEntry.query.filter_by(
        item_type = ItemType.CHECKOUT)
    free_query = InventoryEntry.query.filter_by(
        item_type = ItemType.FREE)
    # replaces property quantity for each item
    counts = db.session.query(Item.entry_id, func.count(Item.entry_id))\
            .group_by(Item.entry_id)\
            .filter_by(user_id = None)\
            .all()
    counts = {id_: count for (id_, count) in counts}

    if user:
        requests = Request.query.filter(Request.user == user,
            Request.status.in_(
            [RequestStatus.APPROVED,
            RequestStatus.SUBMITTED,
            RequestStatus.DENIED])).all()
    else:
        requests = [] # if not logged in, we have no requests to display

    if user and user.is_admin:
        return render_template('pages/inventory.html',
            lottery_items = lottery_query.all(),
            checkout_items = checkout_query.all(),
            free_items = free_query.all(),
            counts = counts,
            requests = requests,
            RequestStatus=RequestStatus, user=user)
    else:
        return render_template('pages/inventory.html',
            lottery_items = lottery_query.filter_by(is_visible = True).all(),
            checkout_items = checkout_query.filter_by(is_visible = True).all(),
            free_items = free_query.filter_by(is_visible = True).all(),
            counts = counts,
            requests = requests,
            RequestStatus=RequestStatus, user=user)

@app.route('/inventory/<int:id>')
@requires_admin()
def inventory_display(id):
    """Render information for admins about an item entry and allow 
    them to edit it."""
    entry = InventoryEntry.query.get(id)
    return render_template('pages/item.html', item = entry, user=user,
            requests = Request.query.filter(
                (Request.status == RequestStatus.APPROVED) | (Request.status == RequestStatus.SUBMITTED)) \
                .join(InventoryEntry.requests).filter(InventoryEntry.id == entry.id),
            RequestStatus = RequestStatus,
            is_lottery = (entry.item_type == ItemType.LOTTERY),
            users = User.query.filter(User.items.any(entry = entry)))

@app.route('/inventory/subitem/delete/<int:id>', methods=['POST'])
@requires_admin()
def delete_subitem(id):
    """Deletes Item if not checked out, returns status"""
    item = Item.query.get(id)
    if item.user_id is not None:
        return jsonify(
            success=False,
            message='Can\'t delete an item that\'s currently checked out!'
        )         

    if item.entry.quantity <= 0: 
        return jsonify(
            success=False,
            message='Can\'t delete this item until you deny a request!'
        )         

    Item.query.filter_by(id=id).delete()
    db.session.commit()

    return jsonify(
        success=True,
    ) 

@app.route('/inventory/subitem/update/<int:id>', methods=['POST'])
@requires_admin()
def update_subitem(id):
    """Updates name of Item, returns status"""
    subitem_to_update = Item.query.filter_by(id=id).first()
    subitem_to_update.item_id = request.form['newSubitemId']
    db.session.commit()

    return jsonify(
        success=True,
    ) 

@app.route('/inventory/subitem/add/<int:id>', methods=['POST'])
@requires_admin()
def add_subitem(id):
    """Creates new subitem, returns status
    
    id -- id of InventoryEntry to add Item to 
    """
    subitem_id = request.form['newSubitemId']
    if subitem_id is None or len(subitem_id) == 0:
        return jsonify(
            success=False,
            message='You need a subitem name!'
        ) 
    # new_subitem = Item(entry_id=id, item_id=str(subitem_id))
    new_subitem = Item(InventoryEntry.query.get(id), subitem_id)
    db.session.add(new_subitem)
    db.session.commit()

    return jsonify(
        success=True,
        id=new_subitem.id
    ) 

def run_item_lottery(item):
    """Run lottery for an item, return True if successful, otherwise False

    item -- instance of InventoryEntry to lottery
    """
    proposals = Request.query.filter(Request.items.any(entry_id = item.id),
            Request.status == RequestStatus.SUBMITTED).all()

    # shuffle proposals
    random.shuffle(proposals)

    qty_to_approve = item.quantity
    if qty_to_approve > len(proposals):
        qty_to_approve = len(proposals)
    
    # approve the first 'qty_to_approve' items in shuffled list
    for proposal in proposals[:qty_to_approve]:
        request_update(proposal.id, RequestStatus.APPROVED)
    if app.config['DENY_LOTTERY_LOSERS']:
        for proposal in proposals[qty_to_approve:]:
            request_update(proposal.id, RequestStatus.DENIED)

    if app.config['CLOSE_LOTTERY_WHEN_RUN']:
        item.item_type = ItemType.CHECKOUT
        db.session.commit()

    return True

@app.route('/inventory/lottery/<int:id>', methods=['POST'])
@requires_admin()
def run_lottery(id):
    """Route to run lottery, returns status
    
    id -- id of InventoryEntry to lottery
    """
    entry = InventoryEntry.query.get(id)
    run_item_lottery(entry)
    return jsonify(
        success=True,
    ) 

@app.route('/inventory/lottery/all', methods=['POST'])
@requires_admin()
def run_all_lotteries():
    """Route that runs lottery for all lottery-able items, returns status"""
    lottery_items = InventoryEntry.query.filter_by(
        item_type = ItemType.LOTTERY).all()
    for item in lottery_items:
        run_item_lottery(item)

    return jsonify(
        success=True,
    ) 

def create_item(form):
    """Adds InventoryEntry to DB based on form, returns created 
    instance of InventoryEntry

    form -- instance of InventoryForm
    """
    if form.item_type.data == 'free':
        item_type = ItemType.FREE
    elif form.item_type.data == 'checkout':
        item_type = ItemType.CHECKOUT
    elif form.item_type.data == 'lottery':
        item_type = ItemType.LOTTERY

    image = url_for('static', filename='images/default.png')
    if form.image.data != '': image = form.image.data
    
    quantity = 1
    if form.quantity.data != None: quantity = form.quantity.data

    item = InventoryEntry(form.name.data,
                          form.description.data,
                          form.link.data,
                          form.category.data,
                          [],
                          image,
                          quantity,
                          item_type)

    item.is_visible = form.visible.data
    return item

@app.route('/inventory/add', methods=['POST'])
@requires_admin()
def inventory_add():
    """Add new InventoryEntry to database, returns status"""
    form = InventoryForm(request.form)
    if form.validate(): 
        item = create_item(form)
        db.session.add(item)
        db.session.commit()
        return jsonify(
            success=True,
        ) 

    errors = '<br>'.join([
        field.title() + ': ' + ', '.join(error) for field, error in form.errors.items()
    ])
    return jsonify(
        success=False,
        message=errors,
    ) 

@app.route('/inventory/autoadd', methods=['POST']) 
@requires_admin()
def inventory_autoadd():
    """Adds instances of InventoryEntry to DB from spreasheet
    takes in URL to Google Sheet via 'url' form parameter
    Returns status
    """
    try:
        list_of_items = get_csv(request.form['url'])
    except SheetsImportError as e:
        return jsonify(
            success=False,
            message=e.msg
        )

    # iterate through the list and add each item the the database
    for index, data in enumerate(list_of_items):
        try:
            if ('visible' in data and
                data['visible'].lower() in ['f', 'false', 'no', 'n']):
                data['visible'] = 'false'
            else:
                data['visible'] = 'true'
            form = InventoryForm(MultiDict(data))
        except TypeError:
            return jsonify(
                success=False,
                message='Something went wrong! Please check your \
                sheet formatting and try again.'
            )

        if form.validate():
            item = create_item(form)
            db.session.add(item)
        else:
            errors = 'Error on row %d:<br>' % (index + 2)
            errors += '<br>'.join([
                field.title() + ': ' + ', '.join(error) for field, error in form.errors.items()
            ])
            return jsonify(
                success=False,
                message=errors
            )

    db.session.commit()

    return jsonify(
        success=True,
    )

@app.route('/inventory/update/<int:id>', methods=['POST'])
@requires_admin()
def inventory_update(id):
    """Updates InventoryEntry fields, returns status"""
    form = InventoryUpdateForm(request.form)
    if form.validate():
        image = form.image.data
        if image == '':
            image = url_for('static', filename='images/default.png')

        item = InventoryEntry.query.get(id)
    
        item.name = form.name.data
        item.description = form.description.data
        item.link = form.link.data
        item.category = form.category.data
        item.image_src = image
        item.is_visible = form.visible.data

        if form.item_type.data == 'free':
            item_type = ItemType.FREE
        elif form.item_type.data == 'checkout':
            item_type = ItemType.CHECKOUT
        elif form.item_type.data == 'lottery':
            item_type = ItemType.LOTTERY

        item.item_type = item_type

        db.session.commit()
        return jsonify(
            success=True
        ) 

    errors = '<br>'.join([
        field.title() + ': ' + ', '.join(error) for field, error in form.errors.items()
    ])
    return jsonify(
        success=False,
        message=errors,
    ) 

@app.route('/inventory/delete/<int:id>', methods=['POST'])
@requires_admin()
def inventory_remove(id):
    """Delete InventoryEntry from database if no associated Items have been
    checked out.

    id -- id of InventoryEntry instance to delete
    """
    entry = InventoryEntry.query.get(id)
    for item in entry.items:
        if item.user != None:
            return jsonify(
                success=False,
                message='Can\'t delete, a user has item checked out!'
            )

    for request in entry.requests:
        db.session.delete(request)

    for item in entry.items:
        db.session.delete(item)
    
    db.session.delete(entry)
    db.session.commit()
    return jsonify(
        success=True
    )

@app.route('/inventory/return/<int:id>', methods=['POST'])
@requires_admin()
def inventory_return(id):
    """Unclaims item from user

    id -- specifies ITEM id *not* entry id
    
    Returns status and whether or not the user should
    have their ID returned
    """
    item = Item.query.get(id)
    user = item.user
    item.user = None
    return_id = False

    if not user.requires_id():
        user.have_their_id = False
        return_id = True
        
    db.session.commit()

    return jsonify(
        success=True,
        return_id=return_id
    )

