from hardwarecheckout.models import db
from sqlalchemy.dialects import postgresql
from sqlalchemy.sql import func

from hardwarecheckout.models.item import Item
from hardwarecheckout.models.request_item import RequestItem
import hardwarecheckout.models.request 
import enum

class ItemType(enum.Enum):
    LOTTERY = 0
    CHECKOUT = 1
    FREE = 2
    MLH = 3

class InventoryEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(120))
    description = db.Column(db.String())
    category = db.Column(db.String())
    link = db.Column(db.String())

    max_request_quantity = db.Column(db.Integer)

    image_src = db.Column(db.String())
    
    item_type = db.Column(db.Enum(ItemType))
    is_visible = db.Column(db.Boolean)
    is_unique = db.Column(db.Boolean)

    items = db.relationship('Item', backref='entry')
    requests = db.relationship('Request', secondary=RequestItem.__table__, 
        lazy='select', viewonly=True)

    def __init__(self, name, description, link, category, tags, 
            image, qty, item_type = ItemType.FREE, max_request_qty = 3):
        self.name = name
        self.description = description 
        self.link = link
        self.category = category
        self.tags = tags
        self.image_src = image

        self.items = []
        for i in range(int(qty)):
            self.items.append(
                    Item(self, self.name + " " + str(i+1)))

        self.max_request_quantity = max_request_qty 

        self.item_type = item_type 
        self.is_visible = True
        self.is_unique = False

    @property
    def quantity(self):
        """Returns quantity of items that have not been 'claimed' by a request"""
        requests = RequestItem.query \
                    .filter_by(entry_id=self.id) \
                    .join(hardwarecheckout.models.request.Request) \
                    .filter_by(status=hardwarecheckout.models.request.RequestStatus.APPROVED) \
                    .with_entities(func.sum(RequestItem.quantity)).scalar()
        if not requests: requests = 0

        return Item.query.filter_by(entry_id = self.id, user = None).count() - requests

    @property
    def submitted_request_quantity(self):
        """Returns number of submitted requests for this entry"""
        requests = RequestItem.query \
            .filter_by(entry_id=self.id) \
            .join(hardwarecheckout.models.request.Request) \
            .filter_by(status=hardwarecheckout.models.request.RequestStatus.SUBMITTED).count()
        return requests

    @property
    def requires_checkout(self):
        return self.item_type == ItemType.CHECKOUT

    @property
    def requires_lottery(self):
        return self.item_type == ItemType.LOTTERY

    @property
    def requires_mlh(self):
        return self.item_type == ItemType.MLH

    def __str__(self): return str(self.name) + " [" + str(self.id) + "]"