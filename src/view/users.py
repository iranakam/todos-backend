from flask import jsonify, make_response
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from src.database import db
from src.lib.request import generate_token, payload, verify_token
from src.lib.validate import user_validate
from src.model.user import User, UserSchema


class Users(Resource):

    @payload
    @user_validate
    def post(request, self):
        schema = UserSchema(exclude=['id', 'created_at', 'updated_at'], many=False)
        try:
            user = schema.load(request.payload, session=db.session)
            user.password = generate_password_hash(user.password)
        except BaseException:
            return make_response(request.payload, 400)
        db.session.add(user)
        db.session.commit()
        return make_response({'user': schema.dump(user), 'token': generate_token(user.id)}, 201)

    @verify_token
    @payload
    @user_validate
    def put(request, self):
        if request.user.id is None:
            return make_response('{"message": "Request is invalid."}', 400)
        schema = UserSchema(exclude=['id', 'created_at', 'updated_at'], many=False)
        try:
            user = schema.load(request.payload, instance=User.query.get(
                request.user.id), partial=True)
            user.password = generate_password_hash(user.password)
        except BaseException:
            return make_response('{"message": "Request is invalid."}', 400)
        db.session.add(user)
        db.session.commit()
        return make_response(jsonify(schema.dump(user)), 200)

    @verify_token
    @payload
    def delete(request, self):
        user = User.query.get(request.payload['id'])
        db.session.delete(user)
        db.session.commit()
        return make_response('', 204)
