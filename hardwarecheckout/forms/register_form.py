from wtforms import Form, StringField, PasswordField, FileField, validators

class RegisterForm(Form):
    email = StringField('email_address', [validators.input_required(), validators.email()])
    password = PasswordField('password', [validators.input_required(), validators.length(min=6), validators.equal_to('confirm', message='Passwords must match')])
    confirm = PasswordField('confirm', [validators.input_required(), validators.length(min=6)])