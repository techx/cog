import pytz
import os

from flask import Flask
from flask_socketio import SocketIO
from urllib.parse import urlsplit
from flaskext.markdown import Markdown

from cog.utils import display_date, deltatimeformat
from cog.models.socket import Socket
from flask_sslify import SSLify

app = Flask(__name__)

import cog.config as config

def get_conf_bool(variable):
    val = os.environ.get(variable, getattr(config, variable))
    if type(val) == bool: return val

    if val == 'True':
        return True
    elif val == 'False':
        return False
    else:
        raise TypeError

def set_conf_bool(app, variable):
    app.config[variable] = get_conf_bool(variable)

def set_conf_str(app, variable):
    app.config[variable] = os.environ.get(variable, getattr(config, variable))

def set_conf_int(app, variable):
    app.config[variable] = int(os.environ.get(variable, getattr(config, variable)))

app.config['SQLALCHEMY_DATABASE_URI'] = config.DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

set_conf_str(app, 'HACKATHON_NAME')
app.config['APP_NAME'] = app.config['HACKATHON_NAME'] + ' Hardware Checkout'

# Debug
app.config['TEMPLATES_AUTO_RELOAD'] = True
set_conf_bool(app, 'DEBUG')

# Jinja Custom Filters
app.jinja_env.filters['datetimefilter'] = display_date
app.jinja_env.filters['deltatime'] = deltatimeformat

# Event specific config settings
set_conf_bool(app, 'CLOSE_LOTTERY_WHEN_RUN')
set_conf_bool(app, 'DISPLAY_LOTTERY_QUANTITY')
set_conf_bool(app, 'DISPLAY_CHECKOUT_QUANTITY')
set_conf_bool(app, 'ENABLE_WAITLIST')
set_conf_bool(app, 'LOTTERY_MULTIPLE_SUBMISSIONS')
set_conf_bool(app, 'LOTTERY_REQUIRES_PROPOSAL')
set_conf_bool(app, 'DENY_LOTTERY_LOSERS')
set_conf_str(app, 'LOTTERY_TEXT')
set_conf_str(app, 'CHECKOUT_TEXT')
set_conf_str(app, 'FREE_TEXT')
set_conf_int(app, 'LOTTERY_CHAR_LIMIT')

from cog.models import db
db.app = app
db.init_app(app)

# enables use of markdown jinja filter
Markdown(app)

if get_conf_bool("FORCE_SSL"):
    SSLify(app)

socketio = SocketIO()
socketio.init_app(app)

import cog.controllers # registers controllers

# delete stale sockets from previous open sessions
try: 
    Socket.query.delete()
    db.session.commit()
except: 
    # exception if DB not yet initialized
    pass