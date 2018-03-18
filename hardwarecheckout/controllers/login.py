from hardwarecheckout import app
from hardwarecheckout import config
from hardwarecheckout.models.user import * 
from hardwarecheckout.utils import verify_token
import requests
import datetime
import json
from urlparse import urljoin
from hardwarecheckout.forms.login_form import LoginForm
from flask import (
    redirect,
    render_template,
    request,
    url_for
)

@app.route('/login')
def login_page():
    """If not logged in render login page, otherwise redirect to inventory"""
    if 'jwt' in request.cookies:
        try:
            decode_token(request.cookies['jwt'])
            return redirect('/inventory')
        except Exception as e:
            pass
        
    return render_template('pages/login.html')

@app.route('/login', methods=['POST'])
def login_handler():
    """Log user in"""
    form = LoginForm(request.form)
    if form.validate():
        url = urljoin(config.QUILL_URL, '/auth/login')
        r = requests.post(url, data={'email':request.form['email'], 'password':request.form['password']})
        try: 
            r = json.loads(r.text)
        except ValueError as e:
            return render_template('pages/login.html', error=[str(e)])
        
        if 'message' in r:
            return render_template('pages/login.html', error=[r['message']])

        quill_id = verify_token(r['token'])
        if not quill_id:
            return render_template('pages/login.html', error=['Invalid token returned by registration'])
        
        if User.query.filter_by(quill_id=quill_id).count() == 0: 
            user = User(quill_id, request.form['email'], r['user']['admin'])
            db.session.add(user)
            db.session.commit()

        response = app.make_response(redirect('/inventory'))
        response.set_cookie('jwt', r['token'])
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