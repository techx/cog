import os

TEST_DB="sqlite:///test_db"
os.environ['DATABASE_URL'] = TEST_DB # sets DB URL for this process 

import hardwarecheckout 
from hardwarecheckout.config import SECRET
import unittest
from jose import jws
import tempfile
import random
import string
from utils import * 

from hardwarecheckout.models import db
from hardwarecheckout.models.user import User
from hardwarecheckout.models.inventory_entry import InventoryEntry
from hardwarecheckout.models.inventory_entry import ItemType 
from hardwarecheckout.models.request import Request 
from hardwarecheckout.models.request import RequestStatus
from hardwarecheckout.models.request_item import RequestItem
from flask import url_for, json
import pytest

@pytest.fixture
def app():
    hardwarecheckout.app.config['TESTING'] = True
    hardwarecheckout.app.config['DEBUG'] = False
    app = hardwarecheckout.app.test_client()
    with hardwarecheckout.app.app_context():
        db.drop_all()
        db.create_all()
        db.app = hardwarecheckout.app
        db.init_app(hardwarecheckout.app)
        ctx = hardwarecheckout.app.test_request_context() 
        ctx.push()
        yield app
        ctx.pop()
        db.session.remove()
        db.drop_all()

@pytest.fixture
def user(app):
    quill_id = ''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(10))
    token = jws.sign(quill_id, SECRET, algorithm='HS256')
    user = User(quill_id, 'alyssap@hacker.org', False)
    db.session.add(user)
    db.session.commit()
    app.set_cookie('localhost:8000', 'jwt', token) 

    return user

@pytest.fixture
def admin(app, user):
    user.is_admin = True
    db.session.commit()
    return user

@pytest.fixture
def item(app):
    item = InventoryEntry('Item', 'Wow lick my socks', 
        'http://test.co', 'Item', [], '', 3)        
    db.session.add(item)
    db.session.commit()
    return item

def test_home(app):
    with captured_templates(hardwarecheckout.app) as templates:
        rv = app.get('/', follow_redirects = True)
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'pages/inventory.html'
        assert len(context['lottery_items']) == 0
        assert len(context['checkout_items']) == 0
        assert len(context['free_items']) == 0

def test_quill_login(app):
    with captured_templates(hardwarecheckout.app) as templates:
        rv = quill_login(app, 'admin@example.com', 'party')
        assert rv.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'pages/inventory.html'

    with captured_templates(hardwarecheckout.app) as templates:
       rv = quill_login(app, 'admin@example.com', 'prty')
       assert rv.status_code == 200
       assert len(templates) == 1
       template, context = templates[0]
       assert template.name == 'pages/login.html'
       assert "That's not the right password." in context['error']

    with captured_templates(hardwarecheckout.app) as templates:
       rv = quill_login(app, 'admin@example.co', 'party')
       assert rv.status_code == 200
       assert len(templates) == 1
       template, context = templates[0]
       assert template.name == 'pages/login.html'
       assert "We couldn't find you!" in context['error']

def test_request_item(app, user, item):
    update_user(app)

    rv = request_item(app, 0)
    response = json.loads(rv.data)
    assert response['success'] == False
    rv = request_item(app, 1)
    response = json.loads(rv.data)
    assert response['success'] == True 

def test_update_user(app, user):
    rv = update_user(app)
    response = json.loads(rv.data)
    assert response['success'] == True 

def test_add_delete_item(app, admin):
    rv = add_item(app) 
    assert json.loads(rv.data)['success'] == True 

    rv = app.get('/inventory/delete/1')
    # TODO: add back check

def test_view_request(app, admin):
    with captured_templates(hardwarecheckout.app) as templates:
        rv = app.get('/request', follow_redirects=True)
        template, context = templates[0]
        assert rv.status_code == 200
        assert template.name == 'pages/admin.html'
        assert len(context['submitted_requests']) == 0

def test_run_lottery(app, admin, item):
    item.item_type = ItemType.LOTTERY
    for _ in range(item.quantity +  3):
        request_item = RequestItem(item, 1)
        request = Request([request_item], admin.id, proposal='Test')
        db.session.add(request_item)
        db.session.add(request)
    db.session.commit()

    rv = app.post(url_for('run_lottery', id=item.id))

    assert json.loads(rv.data)['success'] == True 
    assert RequestItem.query.filter_by(entry_id=item.id) \
            .join(Request).filter_by(status=RequestStatus.APPROVED).count() == 3

def test_run_all_lotteries(app, admin):
    for _ in xrange(3):
        item = InventoryEntry('Item' + str(_), 'Wow lick my socks', 
            'http://test.co', 'Item', [], '', 3, item_type=ItemType.LOTTERY)        
        db.session.add(item)
        for _ in range(item.quantity +  3):
            request_item = RequestItem(item, 1)
            request = Request([request_item], admin.id, proposal='Test')
            db.session.add(request_item)
            db.session.add(request)
    db.session.commit()

    rv = app.post(url_for('run_all_lotteries'))

    assert json.loads(rv.data)['success'] == True 
    items = InventoryEntry.query.all()
    for item in items:
        assert RequestItem.query.filter_by(entry_id=item.id) \
                .join(Request).filter_by(status=RequestStatus.APPROVED).count() == 3

def test_quantities_correct(app, admin):
    def quantities_correct(expected_counts):
        """ Checks that loading the index page produces expected quantities.
            expected_counts - a list of tuples with form
                                (inventory_entry_name, count)
        """
        with captured_templates(hardwarecheckout.app) as templates:
            rv = app.get('/', follow_redirects=True)
            counts = templates[0][1]["counts"]
            for (name, num) in expected_counts:
                id_ = InventoryEntry.query.filter_by(name=name).one().id
                actual_quant = counts.get(id_, 0)
                if actual_quant != num:
                    print("Unexpected quantity {} for item {}".format(actual_quant,
                                                                      name))
                    return False
        return True

    # add item with 1, item with 0 and item with 5 to the database
    item_0_quant = InventoryEntry('Item0', 'Wow lick my socks',
                                  'http://test.co', 'Item', [], '', 0)
    item_1_quant = InventoryEntry('Item1', 'Wow lick my socks',
                                  'http://test.co', 'Item', [], '', 1)
    item_5_quant = InventoryEntry('Item5', 'Wow lick my socks',
                                  'http://test.co', 'Item', [], '', 5)
    db.session.add(item_0_quant)
    db.session.add(item_1_quant)
    db.session.add(item_5_quant)

    # Confirm on index page that quantities are correct
    expected_initial_quantities = [('Item0', 0), ('Item1', 1), ('Item5', 5)]
    assert quantities_correct(expected_initial_quantities)

    # needed to request_items
    update_user(app)

    # request and approve each item
    ids = [entry.id for entry in InventoryEntry.query.all()]
    for id_ in ids:
        request_item(app, id_)
    ids = [req.id for req in Request.query.all()]
    for id_ in ids:
        approve_request(app, id_)

    # confirm updated quantities correct
    expected_post_quantities = [('Item0', 0), ('Item1', 0), ('Item5', 4)]
    assert quantities_correct(expected_post_quantities)
