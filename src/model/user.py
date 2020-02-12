from marshmallow import INCLUDE
from wtforms import PasswordField, StringField, validators

from src.database import db
from src.model.base import Form, Schema


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('NOW()'))
    updated_at = db.Column(db.DateTime,
                           nullable=False,
                           server_default=db.text('CURRENT_TIMESTAMP'),
                           server_onupdate=db.text('CURRENT_TIMESTAMP'))


class UserSchema(Schema):

    class Meta:
        model = User
        unknown = INCLUDE
        fields = ('id', 'name', 'email', 'password',
                  'created_at', 'updated_at')


class UserForm(Form):
    name = StringField('User Name', [
        validators.InputRequired(message='Name is required'),
        validators.Length(
            1, 255, message='Name must be between %(min)d and %(max)d chars')
    ])
    email = StringField('Email', [
        validators.InputRequired(message='Email is required'),
        validators.Email(message='Email is invalid')
    ])
    password = PasswordField('New Password', [
        validators.InputRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
    password_confirm = PasswordField('Repeat Password')
