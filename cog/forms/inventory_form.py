from wtforms import Form, StringField, BooleanField, IntegerField, SelectField, validators
from cog.forms.inventory_update_form import InventoryUpdateForm
from cog.models.inventory_entry import ItemType

def validate_quantity(form, field):
    return field.data != None or form.item_type == ItemType.FREE or form.item_type == ItemType.MLH

class InventoryForm(InventoryUpdateForm):
   quantity = IntegerField('quantity', [validators.Optional(), validators.NumberRange(min=0), validate_quantity])
