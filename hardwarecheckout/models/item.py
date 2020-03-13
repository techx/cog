from hardwarecheckout.models import db

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    item_id = db.Column(db.String())
    entry_id = db.Column(db.Integer, db.ForeignKey('inventory_entry.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
  
    def __init__(self, entry, id):
        self.user = None
        self.entry = entry
        self.item_id = id