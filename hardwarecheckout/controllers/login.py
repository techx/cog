from hardwarecheckout import app
from hardwarecheckout import config
from hardwarecheckout.models.user import * 
from hardwarecheckout.utils import verify_token, gen_uuid, send_verification_email, gen_token
import requests
import datetime
import json
import uuid
from urlparse import urljoin
from hardwarecheckout.forms.login_form import LoginForm
from hardwarecheckout.forms.register_form import RegisterForm
from flask import (
    redirect,
    render_template,
    request,
    url_for
)
from werkzeug.security import generate_password_hash, \
     check_password_hash

@app.route('/verify')
def verify_page():
    if request.args.get('token'):
        user = User.query.filter_by(verification_token=request.args.get('token')).first()
        if user:
            user.verified_email = True
            db.session.commit()
            response = app.make_response(redirect('/login?v=1'))
            return response

    return "Token not found", 400

@app.route('/register')
def register_page():
    # Check if already logged in
    if 'jwt' in request.cookies:
        try:
            decode_token(request.cookies['jwt'])
            return redirect('/inventory')
        except Exception as e:
            pass

    return render_template('pages/register.html')

@app.route('/register', methods=['POST'])
def register_handler():
    form = RegisterForm(request.form)
    if form.validate():
        if User.query.filter_by(email=request.form['email']).first():
            return render_template('pages/register.html', error=["Email address already in use"])
        verification_token = uuid.uuid4().hex
        user = User(gen_uuid(), request.form['email'], generate_password_hash(request.form['password']), verification_token, False)
        db.session.add(user)
        db.session.commit()
        send_verification_email(request.form['email'], verification_token)
        response = app.make_response(redirect('/login?r=1'))
        return response
    errors = []
    for field, error in form.errors.items():
        errors.append(field + ": " + "\n".join(error) + "\n")

    return render_template('pages/register.html', error=errors)

@app.route('/login')
def login_page():
    """If not logged in render login page, otherwise redirect to inventory"""
    if 'jwt' in request.cookies:
        try:
            decode_token(request.cookies['jwt'])
            return redirect('/inventory')
        except Exception as e:
            pass

    success = None
    if request.args.get('r'):
        success = ["Account created! Check your email to verify your account."]
    elif request.args.get('v'):
        success = ["Account verified! Login to continue."]

    return render_template('pages/login.html', success=success)

@app.route('/login', methods=['POST'])
def login_handler():
    """Log user in"""
    form = LoginForm(request.form)
    if form.validate():
        user = User.query.filter_by(email=request.form['email']).first()

        if not user or not check_password_hash(user.password_hash, request.form['password']):
            return render_template('pages/login.html', error=["Invalid username or password"])

        if not user.verified_email:
            return render_template('pages/login.html', error=["Please verify your email to login"])

        response = app.make_response(redirect('/inventory'))
        response.set_cookie('jwt', gen_token(user.quill_id))
        return response
    
    errors = []
    for field, error in form.errors.items():
        errors.append(field + ": " + "\n".join(error) + "\n")

    return render_template('pages/login.html', error=errors)

@app.route('/logout')
def logout():
    """Log user out"""
    response = app.make_response(redirect('/'))
    response.set_cookie('jwt', '')
    return response