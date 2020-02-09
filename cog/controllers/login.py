from cog import app
from cog.config import SECRET, EVENT_SLUG
from cog.models.user import * 
from cog.utils import get_profile_from_jwt
import requests
import datetime
import json
from urllib.parse import urljoin
from flask import (
    redirect,
    render_template,
    request,
    url_for
)
import os

def check_role(roles, role):
    return any(
        d['event_slug'] == EVENT_SLUG and 
        d['role'] == role 
        for d in roles
    )

def get_hacker(token, is_organizer):
    if is_organizer == False:
        req = requests.get('https://hackerapi.com/v2/events/hackthenorth2019/applications/me?token=' + token)
        if req.ok:
            r = json.loads(req.text)
            return r
    return dict()

COOKIE_NAME = '__hackerapi-token-client-only__'

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'GET':
        response = app.make_response(render_template('pages/login.html'))
        return response
    # POST

    jwt = request.headers.get('Authorization')
    # Attempt to grab the user details
    profile, _ = get_profile_from_jwt(jwt)
    if not profile:
        return 'unauthorized jwt', 401
    is_organizer = "admin" in profile.get("groups", [])

    if not is_organizer and profile.get("status") != "admission_confirmed":
        return 'user is not admin or ADMISSION_CONFIRMED status', 403

    hackerapi_id = profile["id"]

    first_name = profile.get("first_name", "")
    last_name = profile.get("last_name", "")
    name = first_name + " " + last_name
    email = profile.get("email")

    user = User.query.filter_by(hackerapi_id=hackerapi_id).first()

    if user == None:
        user = User(hackerapi_id, email, name, None, is_organizer)
        user.first_name = first_name
        user.last_name = last_name
        db.session.add(user)
    else: 
        if name != '':
            user.name = name 
        user.email = email
        user.is_organizer = is_organizer

    db.session.commit()

    response = app.make_response("")
    response.set_cookie('jwt', jwt)
    return response
    
    # Send user to error page.
    # response = app.make_response(render_template('pages/login.html?error=1'))
    # return response
    

@app.route('/logout')
def logout():
    """Log user out"""
    response = app.make_response(redirect(os.getenv("LOGIN_URL") + "/logout"))
    return response