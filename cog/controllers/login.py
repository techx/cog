from cog import app
from cog.config import SECRET, EVENT_SLUG
from cog.models.user import * 
from cog.utils import verify_token
from jose import jws
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

def check_role(roles, role):
    return any(
        d['event_slug'] == EVENT_SLUG and 
        d['role'] == role 
        for d in roles
    )

COOKIE_NAME = '__hackerapi-token-client-only__'

@app.route('/login')
def login_page():
    """If not logged in render login page, otherwise redirect to inventory"""
    if 'jwt' in request.cookies:
        try:
            decode_token(request.cookies['jwt'])
            return redirect('/inventory')
        except Exception as e:
            pass 

    token = request.cookies.get(COOKIE_NAME, '')
    if True: #token != '':
        # Attempt to grab the user details
        # r = json.loads(requests.get('https://hackerapi.com/v2/users/me?token=' + token).text)
        r = json.loads("""
            {
                "id": 1850,
                "email": "kevin.pei@hackthenorth.com",
                "event_roles": [{
                    "event_slug": "hackthenorth2019",
                    "role": "organizer"
                }],
                "name": "Kevin Pei",
                "phone_number": "111-222-3333"
            }
        """)
        if 'id' in r and 'email' in r and 'event_roles' in r:

            event_roles = r['event_roles']
            is_organizer = check_role(event_roles, 'organizer')
            is_hacker = check_role(event_roles, 'hacker') 

            if is_organizer or is_hacker:

                hackerapi_id = str(r['id'])

                name = r.get('legal_name', r.get('name', ''))
                email = r['email']
                phone = r.get('phone_number', '')

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

                token = jws.sign(hackerapi_id.encode('utf-8'), SECRET, algorithm='HS256')

                response = app.make_response(redirect('/inventory'))
                response.set_cookie('jwt', token)
                response.set_cookie(COOKIE_NAME, '')

                return response
         
        response = app.make_response(render_template('pages/login.html'))
        response.set_cookie(COOKIE_NAME, '')
        return response
    return redirect('https://auth.hackthenorth.com/?redirect=cog.team.hackthenorth.com/login')
    

@app.route('/logout')
def logout():
    """Log user out"""
    response = app.make_response(redirect('/'))
    response.set_cookie('jwt', '')
    return response