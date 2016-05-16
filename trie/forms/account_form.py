from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import TextField
from wtforms import validators


class AccountForm(Form):
    email = TextField('email', [
        validators.Required(),
        validators.Length(min=6, max=35)
    ])
    password = PasswordField('password', [
        validators.Required(),
        validators.Length(min=6, max=256)
    ])
    signup = SubmitField(label='sign up')
    login = SubmitField(label='log in')
