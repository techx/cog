from hardwarecheckout.models import db

class Socket(db.Model):
    sid = db.Column(db.String(), primary_key=True)
    user = db.relationship('User', back_populates='sockets')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, sid, user):
        self.sid = sid
        self.user = user