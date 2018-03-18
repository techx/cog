from wtforms import Form, StringField, PasswordField, FileField, validators

class LoginForm(Form):
    email = StringField('email_address', [validators.input_required(), validators.Email()])
    password = PasswordField('password', [validators.input_required()])