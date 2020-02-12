from flask import Blueprint
from flask_restful import Api

from src.view import session, tasks, users

bp = Blueprint('api', __name__, url_prefix="/api")
api = Api(bp)

api.add_resource(tasks.Tasks, '/tasks', endpoint='tasks')
api.add_resource(tasks.Tasks, '/tasks/', endpoint='tasks/')
api.add_resource(session.Session, '/session', endpoint='session')
api.add_resource(session.Session, '/session/', endpoint='session/')
api.add_resource(users.Users, '/users', endpoint='users')
api.add_resource(users.Users, '/users/', endpoint='users/')
