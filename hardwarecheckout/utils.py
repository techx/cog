import uuid
from jose import jws
from jose.exceptions import JWSError
import os
import time
from hardwarecheckout.config import *
from hardwarecheckout.constants import *
from hardwarecheckout.models.user import *
from flask import (redirect, request, jsonify, url_for)
from functools import wraps
from datetime import datetime
from babel import dates
import sendgrid
from sendgrid.helpers.mail import Email, Content, Substitution, Mail

def gen_uuid():
    return str(uuid.uuid4()).replace('-', '')

def gen_token(id, duration=604800):
    try:
        expiry = int(time.time()) + duration
        return jws.sign(id, SECRET)
    except JWSError:
        return None

def verify_token(token):
    try:
        return jws.verify(token, SECRET, algorithms=['HS256'])
    except JWSError:
        return None 

def safe_redirect(endpoint, request): 
    if request.method == 'POST': 
        return jsonify(
            success=False,
            message="Redirecting...",
            redirect=url_for(endpoint)
        ), 401
    return redirect(url_for(endpoint))

def send_verification_email(to, token):
    sg = sendgrid.SendGridAPIClient(apikey=SENDGRID_API_KEY)
    from_email = Email("hello@hackgt.com")
    to_email = Email(to)
    subject = "[%s] Verify your email" % (HACKATHON_NAME)
    content = Content("text/html", """
    Thanks for registering for Hardware Checkout at %s! <br>

    Click <a href='%s'>here</a> to verify your email.<br><br>

    With <3,<br><br>

    The %s Team""" % (HACKATHON_NAME, DOMAIN + "/verify?token=" + token, HACKATHON_NAME))
    mail = Mail(from_email, subject, to_email, content)
    response = sg.client.mail.send.post(request_body=mail.get())

def requires_auth():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt' in request.cookies:
                quill_id = verify_token(request.cookies['jwt'])
                if not quill_id:
                    return safe_redirect('login_page', request)
                user = User.query.filter_by(quill_id=quill_id).first()
         
                # if no user found for auth token, log them out (clears token)
                if user == None:
                    return safe_redirect('logout', request)

                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                return safe_redirect('login_page', request)

        return decorated
    return decorator

def auth_optional():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt' in request.cookies:
                quill_id = verify_token(request.cookies['jwt'])
                if not quill_id:
                    f.__globals__['user'] = None 
                    return f(*args, **kwargs)

                user = User.query.filter_by(quill_id=quill_id).first()

                # if no user found for auth token, log them out (clears token)
                if user == None:
                    return safe_redirect('logout', request)

                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                f.__globals__['user'] = None 
                return f(*args, **kwargs)

        return decorated
    return decorator

def requires_admin():
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if 'jwt' in request.cookies:
                quill_id = verify_token(request.cookies['jwt'])
                if not quill_id:
                    return safe_redirect('login_page', request)
                user = User.query.filter_by(quill_id=quill_id).first()

                # if no user found for auth token, log them out (clears token)
                if user == None:
                    return safe_redirect('logout', request)

                if not user.is_admin:
                    return "Must be admin to access this", 403 
                f.__globals__['user'] = user
                return f(*args, **kwargs)
            else:
                return safe_redirect('login_page', request)

        return decorated
    return decorator

# Custom filters
def deltatimeformat(t):
    return dates.format_timedelta(t - datetime.now(), add_direction=True)

def display_date(value):
    tz = pytz.timezone(config.DISPLAY_TIMEZONE)
    aware_utc_dt = value.replace(tzinfo=pytz.utc)
    dt = aware_utc_dt.astimezone(tz)
    return dt.strftime("%b %d, %Y %I:%M %p {tz}".format(tz=dt.tzname()))

def read_csv(csv_text):
    # Parse CSV
    parsed = [line.strip().split(',') for line in csv_text.split('\n')]
    header_count = len(parsed[0])
    ret = [parsed[0]] 
    for p in parsed:
        ret.append(p)
    return {"header": ret[0], "data": ret[2:]}
