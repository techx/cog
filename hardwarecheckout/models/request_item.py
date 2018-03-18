from hardwarecheckout.models import db

class RequestItem(db.Model):
    entry_id = db.Column(db.Integer, db.ForeignKey('inventory_entry.id'), primary_key=True)
    request_id = db.Column(db.Integer, db.ForeignKey('request.id'), primary_key=True)
    quantity = db.Column(db.Integer)

    entry = db.relationship('InventoryEntry')

    def __init__(self, entry, quantity):
        self.entry = entry
        self.quantity = quantity

    def __str__(self):
        return str(self.quantity) + 'x ' + self.entry.name