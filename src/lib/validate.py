import functools

from flask import make_response, request

from src.model.task import TaskForm
from src.model.user import UserForm


def user_validate(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        form = UserForm.from_json(request.get_json(), skip_unknown_keys=True)
        if form.validate() is False:
            return make_response('{"message": "Request is invalid"}', 400)
        return method(*args, **kwargs)

    return wrapper


def task_validate(method):

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        form = TaskForm.from_json(request.get_json(), skip_unknown_keys=True)
        if form.validate() is False:
            return make_response('{"message": "Request is invalid"}', 400)
        return method(*args, **kwargs)

    return wrapper
