import wtforms_json
from flask_marshmallow import Marshmallow
from flask_wtf import FlaskForm
from marshmallow import INCLUDE


wtforms_json.init()

ma = Marshmallow()


class Schema(ma.ModelSchema):

    class Meta:
        unknown = INCLUDE


class Form(FlaskForm):
    pass
