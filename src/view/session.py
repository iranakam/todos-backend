from flask import jsonify, make_response
from flask_restful import Resource

from src.lib.request import check_password, generate_token, payload
from src.model.user import User


class Session(Resource):

    @payload
    def post(req, self):
        if (user := User.query.filter_by(email=req.payload['email']).one()) is None:
            return make_response(req.payload, 401)
        if check_password(user.password, req.payload['password']) is False:
            return make_response('', 401)
        return make_response(jsonify({'id': user.id, 'token': generate_token(user.id)}), 200)

    def option(self):
        pass
