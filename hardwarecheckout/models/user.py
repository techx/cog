from hardwarecheckout.models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    hackerapi_id = db.Column(db.String(), unique=True)
    is_admin = db.Column(db.Boolean)
    location = db.Column(db.String(120))
    name = db.Column(db.String())
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    phone = db.Column(db.String(255))
    email = db.Column(db.String())
    notifications = db.Column(db.Boolean)
    have_their_id = db.Column(db.Boolean)
    requests = db.relationship('Request', back_populates='user')
    # sockets = db.relationship('Socket', back_populates='user')

    items = db.relationship('Item', backref='user')

    def __init__(self, hackerapi_id, email, name, phone, is_admin):
        self.hackerapi_id = hackerapi_id
        self.email = email
        self.is_admin = is_admin
        self.name = name
        self.phone = phone
        self.location = ''
        self.notifications = False
        self.have_their_id = False

    def requires_id(self):
        for item in self.items:
            if item.entry.requires_checkout \
                or item.entry.requires_lottery:
                return True
        
        return False