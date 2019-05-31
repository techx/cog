from cog import app

import os

from flask import (
    send_from_directory,
    request,
    redirect,
    render_template
)
from cog.utils import requires_auth

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.join(app.root_path, 'static'),
        'favicon.ico',
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/')
def index():
    return redirect('/inventory')
