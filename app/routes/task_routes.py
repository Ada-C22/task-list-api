import os
from flask import Blueprint, abort, make_response,request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from .route_utilities import validate_model, create_model
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix = "/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return {"task": create_model(Task, request_body)}, 201

    # try:
    #     new_task = Task.from_dict(request_body)

    # except KeyError as error:
    #     response = {"details": "Invalid data"}
    #     abort(make_response(response, 400))

    # db.session.add(new_task)
    # db.session.commit()

    # response = new_task.to_dict()
    # return {"task": response}, 201

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    
    db.session.commit()
    
    response = task.to_dict()

    return {"task": response}, 200 

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    response = task.to_dict()
    url = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization": f"Bearer {os.environ.get('AUTHORIZATION_TOKEN')}"}
    data = {
    "channel": "task-notification",
    "text": f"Someone just completed the task {task.title}"
}

    slack_response = requests.post(url, json=data, headers=headers)
    return {"task": response}, 200


@tasks_bp.get("")
def get_all_tasks():
    sort_title_param = request.args.get("sort", "asc")

    if sort_title_param == "desc":
        tasks = Task.query.order_by(Task.title.desc())
    else:
        tasks = Task.query.order_by(Task.title.asc())
    
    task_response = [task.to_dict() for task in tasks]

    return task_response, 200

@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]

    if request_body.get("is_complete"):
        task.completed_at = datetime.now()
    else:
        task.completed_at = None

    db.session.commit()

    response = {"task": task.to_dict()}
    return response, 200
    # return Response(status=200, mimetype="application/json")

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task.id} "{task.title}" successfully deleted'}
    return response, 200

