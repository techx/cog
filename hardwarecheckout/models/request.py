from hardwarecheckout.models import db
from hardwarecheckout.models.user import User
from hardwarecheckout.models.inventory_entry import ItemType
from datetime import datetime
import enum

class RequestStatus(enum.Enum):
    SUBMITTED = 0 
    APPROVED  = 1
    FULFILLED = 2
    DENIED    = 3
    CANCELLED = 4

    def __str__(self):
        return self.name

class Request(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    items = db.relationship('RequestItem', backref='request')

    status = db.Column(db.Enum(RequestStatus))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    requires_id = db.Column(db.Boolean)
    requires_lottery = db.Column(db.Boolean)

    user = db.relationship('User', back_populates='requests')

    proposal = db.Column(db.String())

    def __init__(self, items, user_id, proposal=''):
        self.status = RequestStatus.SUBMITTED 
        self.items = items
        self.requires_id = self.check_requires_id()
        self.requires_lottery = self.check_requires_lottery()
        self.user_id = user_id 
        self.user = User.query.get(user_id) 
        self.timestamp = datetime.now()
        self.proposal = proposal

    def __str__(self):
        return self.user.email + ' ' + str(self.status) \
            + ' ' + ', '.join([str(i) for i in self.items])
      
    def check_requires_id(self):
        for item in self.items:
            if (item.entry.item_type == ItemType.LOTTERY 
                or item.entry.item_type == ItemType.CHECKOUT): 
                return True
        
        return False

    def check_requires_lottery(self):
        for item in self.items:
            if item.entry.item_type == ItemType.LOTTERY:
                return True

        return False