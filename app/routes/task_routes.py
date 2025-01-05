from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
import os
import requests
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

# SEND SLACK NOTIFICATION
def send_slack_notification(task_title):
    slack_token = os.environ.get("SLACK_BOT_TOKEN")

    url = "https://slack.com/api/chat.postMessage"

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json",
    }

    message_body = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task_title}",
    }

    requests.post(url, headers=headers, json=message_body)


# CREATE
@bp.post("")
def create_task():
    request_body = request.get_json()

    # Check for required fields before calling create_model
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    response = create_model(Task, request_body)
    task_dict = response.get_json()
    return make_response({"task": task_dict}, 201)


# READ ALL
@bp.get("")
def get_all_tasks():

    return get_models_with_filters(Task, request.args)


# READ ONE
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    return {"task": task.to_dict()}, 200


# UPDATE
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return {"task": task.to_dict()}, 200

# DELETE
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    task_title = task.title
    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task_title}" successfully deleted'}, 200

# MARK COMPLETE
@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.mark_complete()

    db.session.commit()

    send_slack_notification(task.title)

    return {"task": task.to_dict()}, 200

# MARK INCOMPLETE
@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.mark_incomplete()

    db.session.commit()

    return {"task": task.to_dict()}, 200
