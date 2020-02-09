from cog import app
# from cog import socketio
from cog.models import db

from cog.models.request import Request, RequestStatus
from cog.models.inventory_entry import InventoryEntry
from cog.models.inventory_entry import ItemType
from cog.models.user import User
from cog.models.item import Item
from cog.models.request_item import RequestItem
# from cog.models.socket import Socket

from cog.utils import requires_auth, requires_admin, verify_token
from sqlalchemy import event

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template,
    jsonify
)

@app.route('/request')
@requires_admin()
def get_requests():
    """Renders requests that are submitted and non lottery OR already approved"""
    return render_template('pages/admin.html',
        submitted_requests = Request.query.filter_by(requires_lottery = False,
        status = RequestStatus.SUBMITTED).all(),
        approved_requests = Request.query.filter_by(status = RequestStatus.APPROVED).all(),
        RequestStatus = RequestStatus,
        lottery_items = InventoryEntry.query.filter_by(item_type=ItemType.LOTTERY).all(),
        user=user)

@app.route('/request/submit', methods=['POST'])
@requires_auth()
def request_submit():
    """Submits new request"""
    proposal = request.form.get('proposal', '')
    requested_quantity = int(request.form.get('quantity', 1))

    if app.config['LOTTERY_CHAR_LIMIT']:
        if len(proposal) > app.config['LOTTERY_CHAR_LIMIT']:
            proposal = proposal[:app.config['LOTTERY_CHAR_LIMIT']]

    entry = InventoryEntry.query.get(request.form['item_id'])
    if not entry:
        return jsonify(
            success=False,
            message='No item with this id!'
        )

    if entry.item_type == ItemType.LOTTERY:
        if len(proposal) == 0 and app.config['LOTTERY_REQUIRES_PROPOSAL']:
            return jsonify(
                success=False,
                message='Proposal required!'
            )
        if not app.config['LOTTERY_MULTIPLE_SUBMISSIONS']:
            request_count = Request.query.filter(
                (Request.user_id == user.id)
                & ((Request.status != RequestStatus.CANCELLED)
                & (Request.status != RequestStatus.FULFILLED))
                ).join(InventoryEntry.requests
                ).filter(InventoryEntry.id == entry.id).count()
            item_posession_count = InventoryEntry.query.filter_by(id = entry.id) \
                .join(Item).filter(Item.user_id == user.id).count()

            # can only enter lottery if you don't have a pending or denied request
            # and you don't currently have the item checked out
            if request_count > 0 or item_posession_count > 0:
                return jsonify(
                    success=False,
                    message='You\'ve already entered this lottery!'
                )

            # can only request one at a time
            requested_quantity = 1

    if entry.quantity < requested_quantity:
        if not app.config['ENABLE_WAITLIST']:
            return jsonify(
                success=False,
                message='Out of stock!'
            )

    for _ in range(requested_quantity):
        item = RequestItem(
            InventoryEntry.query.get(request.form['item_id']),
            1)

        r = Request(
            [item],
            user.id,
            proposal)

        db.session.add(item)
        db.session.add(r)

    db.session.commit()
    return jsonify(
        success=True,
    )

@app.route('/request/<int:id>/cancel', methods=['POST'])
@requires_auth()
def request_cancel(id):
    """Cancel request, returns status
    Non-admins can only cancel own request, returns 403 if attempted"""
    r = Request.query.get(id)
    if user.is_admin or r.user_id == user.id:
        r.status = RequestStatus.CANCELLED
        db.session.commit()
        return jsonify(
            success=True,
        )
    else:
        return jsonify(
            success=False,
            message="Forbidden"
        ), 403

def request_update(id, status):
    """Update status of request, returns True if successful, otherwise False

    id -- id of request
    status -- new status
    """
    r = Request.query.get(id)
    r.status = status
    db.session.commit()
    return True

@app.route('/request/<int:id>/approve', methods=['POST'])
@requires_admin()
def request_approve(id):
    """Approve request and return status"""
    r = Request.query.get(id)
    for request_item in r.items:
        entry = request_item.entry
        quantity = request_item.quantity

        # get items of proper type
        for _ in range(quantity):
            if entry.quantity < quantity:
                return jsonify(
                    success=False,
                    message='Out of stock!'
                )
    request_update(id, RequestStatus.APPROVED)
    return jsonify(
        success=True,
    )

@app.route('/request/<int:id>/fulfill', methods=['POST'])
@requires_admin()
def request_fulfill(id):
    """Fulfill request and return status"""
    r = Request.query.get(id)

    # collect user ID
    if request.form['collected_id'] == 'true':
        collected_id = True
    elif request.form['collected_id'] == 'false':
        collected_id = False
    else:
        return jsonify(
            success=False,
            message="collected_id must be a boolean"
        )

    if r.requires_id and collected_id:
        r.user.have_their_id = True

    for request_item in r.items:
        entry = request_item.entry
        quantity = request_item.quantity

        # get items of proper type
        for _ in range(quantity):
            item = Item.query.filter_by(entry_id = entry.id, user = None).first()
            if item == None:
                return jsonify(
                    success=False,
                    message='Out of stock!'
                )
            # give user item
            r.user.items.append(item)

    # update request status
    request_update(id, RequestStatus.FULFILLED)

    # commit changes to DB
    db.session.commit()

    return jsonify(
        success=True,
    )

@app.route('/request/<int:id>/deny', methods=['POST'])
@requires_admin()
def request_deny(id):
    """Deny request and return status"""
    request_update(id, RequestStatus.DENIED)
    return jsonify(
        success=True,
    )

# @socketio.on('connect', namespace='/admin')
# def authenticate_admin_conection():
#     """Callback when client connects to /admin namespace, returns True
#     if admin and False otherwise
#     """
#     if 'jwt' in request.cookies:
#         hackerapi_id = verify_token(request.cookies['jwt'])
#         if not hackerapi_id:
#             return False
#         user = User.query.filter_by(hackerapi_id=hackerapi_id).first()

#         if user == None or not user.is_admin:
#             return False

#         return True
#     else:
#         return False

# @socketio.on('connect', namespace='/user')
# def authenticate_user_conection():
#     """Callback when client connects to /user namespace, returns True
#     if logged in and False otherwise
#     """
#     if 'jwt' in request.cookies:
#         hackerapi_id = verify_token(request.cookies['jwt'])
#         if not hackerapi_id:
#             return False
#         user = User.query.filter_by(hackerapi_id=hackerapi_id).first()

#         if user == None:
#             return False

#         socket = Socket(request.sid, user)
#         db.session.add(socket)
#         db.session.commit()
#         return True
#     else:
#         return False

# @socketio.on('disconnect', namespace='/user')
# def user_disconnect():
#     """Delete user's socket when they disconnect"""
#     socket = Socket.query.get(request.sid)
#     db.session.delete(socket)
#     db.session.commit()

def on_request_insert(mapper, connection, target):
    """Callback for when new request is inserted into DB"""
    request_change_handler(target.request)

def on_request_update(mapper, connection, target):
    """Callback for when request is modified"""
    request_change_handler(target)

def request_change_handler(target):
    """Handler that sends updated HTML for rendering requests"""
    user = target.user
    # sockets = Socket.query.filter_by(user=user).all()

    requests = Request.query.filter(Request.user == user, Request.status.in_(
        [RequestStatus.APPROVED, RequestStatus.SUBMITTED, RequestStatus.DENIED])).all()

    requests_html = render_template('includes/macros/display_requests.html',
                        requests = requests,
                        RequestStatus = RequestStatus,
                        admin = False,
                        time = False)

    # for socket in sockets:
    #     socketio.emit('update', {
    #         'requests': requests_html,
    #     }, namespace='/user', room=socket.sid)

    # TODO: add check if at least one admin is connected
    approved_requests = render_template('includes/macros/display_requests.html',
            # display requests that are submitted and non lottery OR already approved
            requests = Request.query.filter_by(status = RequestStatus.APPROVED).all(),
            RequestStatus = RequestStatus,
            admin = True,
            time = True)

    submitted_requests = render_template('includes/macros/display_requests.html',
            # display requests that are submitted and non lottery OR already approved
            requests = Request.query.filter_by(requires_lottery = False,
                status = RequestStatus.SUBMITTED).all(),
            RequestStatus = RequestStatus,
            admin = True,
            time = True)

    lottery_items = InventoryEntry.query.filter_by(item_type=ItemType.LOTTERY).all()
    lottery_quantities = []
    for item in lottery_items:
        lottery_quantities.append(
            {
                "id": item.id,
                "available": item.quantity,
                "submitted": item.submitted_request_quantity
            }
        )

    # socketio.emit('update', {
    #     'approved_requests': approved_requests,
    #     'submitted_requests': submitted_requests,
    #     'lottery_quantities': lottery_quantities
    # }, namespace='/admin')

# listeners for change to Request database
event.listen(RequestItem, 'after_insert', on_request_insert)
event.listen(Request, 'after_update', on_request_update)
