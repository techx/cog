from contextlib import contextmanager
from flask import template_rendered

def hackerapi_login(app, username, password):
   return app.post('/login', data=dict(
       email=username,
       password=password
   ), follow_redirects=True)

def logout(app):
    return app.get('/logout', follow_redirects=True)

def add_item(app, quantity=5, lottery=True, checkout=True):
    data=dict(
        name='Fidget Spinner',
        description='Lets you spin like a good fidget boi',
        link='http://fidget.spinner',
        category='Spinner',
        image='', 
        quantity=quantity, 
        item_type='free')

    if lottery:
        data['item_type'] = 'lottery' 
    elif checkout:
        data['item_type'] = 'checkout'

    return app.post('/inventory/add', data=data, follow_redirects=True)

# def update_user(app):
#     return app.post('/user/1/update', data=dict(
#            location='A5',
#            phone='617-555-0123',
#            name='Alyssa'
#        ), follow_redirects=True)

def request_item(app, id):
    return app.post('/request/submit', data=dict(
        item_id=id,
        quantity=1), 
        follow_redirects=True)

def approve_request(app, id_):
    return app.post('/request/{}/approve'.format(id_),
                    follow_redirects=True)

@contextmanager
def captured_templates(app):
    recorded = []
    def record(sender, template, context, **extra):
        recorded.append((template, context))
    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)
