from flask_marshmallow import Marshmallow
from wtforms import DateTimeField, SelectField, StringField, validators

from src.database import db
from src.model.base import Form, Schema


class Task(db.Model):

    __tablename__ = "tasks"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    schedule = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    memo = db.Column(db.Text)
    priority = db.Column(db.Integer, nullable=False, default=5)
    status = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('NOW()'))
    updated_at = db.Column(db.DateTime, nullable=False,
                           server_default=db.text('NOW()'))


ma = Marshmallow()


class TaskSchema(Schema):

    class Meta:
        model = Task
        fields = ('id', 'name', 'schedule', 'memo', 'priority', 'status',
                  'created_at', 'updated_at')


class TaskForm(Form):
    name = StringField('Task name', [
        validators.InputRequired(message='Task name is required'),
        validators.Length(
            1, 255,
            message='Task name must be between %(min)d and %(max)d chars')
    ])
    schedule = DateTimeField('Schedule', format='%Y-%m-%dT%H:%M:%S.%fZ')
    priority = SelectField('Priority', choices=[
                           ('0', '0'), ('1', '1'), ('2', '2')])
