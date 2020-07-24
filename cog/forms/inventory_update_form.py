from wtforms import Form, StringField, BooleanField, IntegerField, SelectField, validators
from cog.models.inventory_entry import ItemType

def validate_image(form, field):
    if field.data == field.default:
        return True
    url_validator = validators.URL()
    return url_validator(form, field) 

class InventoryUpdateForm(Form):
    name = StringField('name', [validators.input_required(), validators.Length(max=120)])
    description = StringField('description', [validators.Optional()])
    link = StringField('link', [validators.Optional(), validators.URL()])
    category = StringField('category', [validators.input_required()])
    image = StringField('image', [validators.Optional(), validate_image], default='/static/images/default.png')
    item_type = SelectField('item_type', [validators.input_required()], 
        choices=[('free', 'Free to Take'), ('checkout', 'Requires Checkout'), ('lottery', 'Requires Lottery'), ('mlh', 'MLH Item')])
    visible = BooleanField('visible')

