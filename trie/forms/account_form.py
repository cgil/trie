from flask_wtf import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms import TextField
from wtforms import validators


class AccountForm(Form):
    email = TextField('email', [
        validators.Required(message="* an email is required"),
        validators.Length(min=3, max=256, message="are you sure that's right?")
    ])
    password = PasswordField('password', [
        validators.Required(message='* a password is required'),
        validators.Length(min=6, max=256, message='* required length of 6 - 256 characters')
    ])
    signup = SubmitField(label='sign up')
    login = SubmitField(label='log in')
