from wtforms import Form, StringField, IntegerField, FileField, validators

class InventoryImportForm(Form):
	name = StringField('name', [validators.input_required(), validators.Length(max=120)])
	description = StringField('description', [validators.Length(max=120)])
	image = FileField(u'image_file')
	quantity = IntegerField('quantity')
	link = StringField('link')
	category = StringField('category')
	requires_checkout = StringField('checkout')
