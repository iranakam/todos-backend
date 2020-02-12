import datetime
import functools

import jwt
from flask import make_response, request
from werkzeug.security import check_password_hash
from flask import current_app

from Crypto.PublicKey import RSA
from src.model.user import User as um


def check_password(x, y):
    return check_password_hash(x, y)


class Request:
    payload = ()
    user = None


def payload(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if type(args[0]) is Request:
            print(request.get_json())
            args[0].payload = request.get_json()
            return method(*args, **kwargs)
        else:
            r = Request()
            r.payload = request.get_json()
            return method(r, *args, **kwargs)

    return wrapper


def args(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if type(args[0]) is Request:
            args[0].args = request.args
            return method(*args, **kwargs)
        else:
            r = Request()
        return method(r, *args, **kwargs)

    return wrapper


def verify_token(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        try:
            decoded = decode(request.headers.get('Authorization'), 'RS256')
            # user = um.query.filter_by(id=decoded['id']).first()
            if (user := um.query.filter_by(id=decoded['id']).one()) is None:
                raise jwt.InvalidTokenError
            if type(args[0]) is Request:
                args[0].user = user
                return method(*args, **kwargs)
            else:
                r = Request()
                r.user = user
                return method(r, *args, **kwargs)
        except jwt.DecodeError:
            return make_response('{"message": "Token is invalid."}', 400)
        except jwt.ExpiredSignatureError:
            return make_response('{"message": "Token is expired."}', 400)

    return wrapper


def generate_token(id, exp=None, key=None, algorithm='RS256'):
    try:
        exp = datetime.datetime.utcnow() + datetime.timedelta(hours=48)
        return encode(id, exp, 'RS256')
    except BaseException:
        return make_response('{"msg": "generate token is failed"}', 500)


def decode(token, algorithm):
    # private_key = RSA.importKey(open('/root/backend/src/lib/private-key.pem').read())
    private_key = RSA.importKey(open(current_app.config['PRIVATE_KEY_PATH']).read())
    key = private_key.publickey().exportKey('PEM')
    return jwt.decode(token, key, algorithm)


def encode(id, exp, algorithm):
    key = open('/root/backend/src/lib/private-key.pem').read()
    return jwt.encode({'id': id, 'exp': exp}, key, algorithm).decode('utf-8')
