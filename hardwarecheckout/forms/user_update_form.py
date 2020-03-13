from wtforms import Form, StringField, validators
from wtforms_alchemy import PhoneNumberField

class UserUpdateForm(Form):
	location = StringField('location', [validators.Length(max=120)])
	phone = PhoneNumberField('phone')
	name = StringField('name', [validators.Length(max=255)])	
	def validate(self):
		res = super(UserUpdateForm, self).validate()
		
		if not res:
			return False	
		for field in [self.location, self.phone, self.name]:
			if field.data:
				return True	
		self.errors['error'] = ['At least one field must be filled to update']
		return False