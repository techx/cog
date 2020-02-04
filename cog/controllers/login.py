from cog import app
from cog.config import SECRET, EVENT_SLUG
from cog.models.user import * 
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

    # if 'jwt' in request.cookies:
    #     try:
    #         decode_token(request.cookies['jwt'])
    #         return redirect('/inventory')
    #     except Exception as e:
    #         pass 

    jwt = request.headers.get('Authorization')
    # Attempt to grab the user details
    try:
        r = requests.get(os.getenv("ENDPOINT_URL") + "/user_profile", headers={"Authorization": jwt})
        profile = r.json()
    except Exception as e:
        print(e)
        return 'unauthorized jwt', 401
    is_organizer = "admin" in profile.get("groups", [])

    if not is_organizer and profile.get("status") != "admission_confirmed":
        return 'user is not admin or ADMISSION_CONFIRMED status', 403

    hackerapi_id = profile["id"]

    name = profile.get("first_name", "") + " " + profile.get("last_name", "")
    email = profile.get("email")
    phone = profile.get("phone")

    user = User.query.filter_by(hackerapi_id=hackerapi_id).first()

    if user == None:
        user = User(hackerapi_id, email, name, phone, is_organizer)
        db.session.add(user)
    else: 
        if name != '':
            user.name = name 
        user.email = email
        if phone != '':
            user.phone = phone 
        user.is_organizer = is_organizer

    db.session.commit()

    return "", 204
    
    # Send user to error page.
    # response = app.make_response(render_template('pages/login.html?error=1'))
    # return response
    

@app.route('/logout')
def logout():
    """Log user out"""
    response = app.make_response(redirect(os.getenv("LOGIN_URL") + "/logout"))
    return response