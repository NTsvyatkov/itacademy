from flask.ext.wtf import Form
from wtforms import TextField, BooleanField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    login = TextField('login', validators = [Required("Enter your username")])
    password = PasswordField('Password', validators = [Required("Enter your password")])
