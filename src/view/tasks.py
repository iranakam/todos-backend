from flask import jsonify, make_response
from flask_restful import Resource

from src.database import db
from src.lib.request import payload, verify_token
from src.lib.validate import task_validate
from src.model.task import Task, TaskSchema


class Tasks(Resource):

    @verify_token
    @payload
    def get(request, self):
        id = None if request.payload is None else request.payload['id']
        task = Task.query.filter_by(user_id=request.user.id).all() \
            if id is None else Task.query.filter_by(id=id, user_id=request.user.id).one()
        schema = TaskSchema(many=True)
        return make_response(jsonify(schema.dump(task)), 200)

    @verify_token
    @payload
    @task_validate
    def post(request, self):
        request_schema = TaskSchema(exclude=['id', 'created_at', 'updated_at'], many=False)
        task = request_schema.load(request.payload, session=db.session)
        task.user_id = request.user.id
        task.status = False
        db.session.add(task)
        db.session.commit()
        response_schema = TaskSchema(exclude=['created_at', 'updated_at'], many=False)
        return make_response(jsonify(response_schema.dump(task)), 201)

    @verify_token
    @payload
    @task_validate
    def put(request, self):
        # TODO: Set timestamp in updated_at at the time of update.
        request_schema = TaskSchema(exclude=['created_at', 'updated_at'], many=False)
        task = request_schema.load(request.payload, instance=Task.query.filter_by(
            id=request.payload['id'], user_id=request.user.id).first(), partial=True)
        db.session.add(task)
        db.session.commit()
        response_schema = TaskSchema(exclude=['created_at', 'updated_at'], many=False)
        return make_response(jsonify(response_schema.dump(task)), 201)

    @verify_token
    @payload
    def delete(request, self):
        if (id:= request.payload['id']) is None:
            return make_response('', 400)
        task = Task.query.filter_by(id=id, user_id=request.user.id).first()
        db.session.delete(task)
        db.session.commit()
        return make_response({'id': id}, 201)
