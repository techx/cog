from hardwarecheckout import app

import os

from hardwarecheckout.utils import requires_auth, requires_admin
from hardwarecheckout.models.user import User
from hardwarecheckout.models.request import Request, RequestStatus
from hardwarecheckout.models import db

from hardwarecheckout.forms.user_update_form import UserUpdateForm

from flask import (
    jsonify,
    send_from_directory,
    request,
    redirect,
    render_template
)

@app.route('/user')
@requires_auth()
def get_user():
    # render user page, with options to change settings etc
    return render_template('pages/user.html',
            requests = Request.query.filter_by(user_id = user.id).order_by(Request.timestamp.desc()).all(),
            user = user,
            isme = True,
            target = user,
            RequestStatus = RequestStatus)

@app.route('/user/<int:id>')
@requires_auth()
def user_items(id):
    # display items signed out by user
    # only works for user if they match id, works for admins
    is_me = (user.id == id)
    target = User.query.get(id)
    return render_template('pages/user.html',
            requests = Request.query.filter_by(user_id = target.id).order_by(Request.timestamp.desc()).all(),
            user = user,
            target = target,
            RequestStatus = RequestStatus,
            isme = is_me,
            items = target.items)

# @app.route('/user/<int:id>/update', methods=['POST'])
# @requires_auth()
# def user_update(id):
#     # update user settings
#     if user.is_admin or user.id == id:
#         user_to_change = User.query.get(id)
#         form = UserUpdateForm(request.form)
#         if form.validate(): 
#             if form.location.data:
#                 user_to_change.location = form.location.data
#             if form.phone.data:
#                 user_to_change.phone = form.phone.data.national_number
#             if form.name.data:  
#                 user_to_change.name = form.name.data
#             db.session.commit()
#             return jsonify(
#                 success=True
#             ) 

#         error_msg = '\n'.join([key.title() + ': ' + ', '.join(value) for key, value in form.errors.items()])

#         return jsonify(
#             success=False,
#             message=error_msg,
#             user={
#                 'phone': user_to_change.phone,
#                 'name': user_to_change.name,
#                 'location': user_to_change.location
#             }
#         )

#     else:
#         return jsonify(
#             success=False,
#             message='Forbidden'
#         ), 403

@app.route('/users')
@requires_admin()
def get_users():
    # render list of all users 
    return render_template('pages/users.html',
            user = user,
            users = User.query.all())