from hardwarecheckout.models import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quill_id = db.Column(db.String(), unique=True)
    verified_email = db.Column(db.Boolean)
    verification_token = db.Column(db.String(), unique=True)
    is_admin = db.Column(db.Boolean)
    location = db.Column(db.String(120))
    name = db.Column(db.String())
    phone = db.Column(db.String(255))
    email = db.Column(db.String())
    password_hash = db.Column(db.String())
    notifications = db.Column(db.Boolean)
    have_their_id = db.Column(db.Boolean)
    requests = db.relationship('Request', back_populates='user')
    sockets = db.relationship('Socket', back_populates='user')

    items = db.relationship('Item', backref='user')

    def __init__(self, quill_id, email, password_hash, verification_token, is_admin):
        self.quill_id = quill_id
        self.email = email
        self.password_hash = password_hash
        self.is_admin = is_admin
        self.name = ''
        self.location = '' 
        self.phone = '' 
        self.notifications = False
        self.have_their_id = False
        self.verified_email = False
        self.verification_token = verification_token

    def requires_id(self):
        for item in self.items:
            if item.entry.requires_checkout \
                or item.entry.requires_lottery:
                return True
        
        return False