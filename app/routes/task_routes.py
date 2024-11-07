from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.db import db
from sqlalchemy import desc
import datetime
import requests
import os
from app.routes.route_utilities import validate_model_id, delete_record, create_model, get_models_with_filters

task_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")


@task_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@task_bp.get("")
def get_all_tasks():
    filter_params = request.args
    return get_models_with_filters(Task, filter_params)


@task_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model_id(Task, task_id)
    task_dict = task.to_dict()
    if task.goal_id:
        task_dict["goal_id"] = task.goal_id
    return {"task": task_dict}, 200


@task_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model_id(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return {"task": task.to_dict()}, 200


@task_bp.delete("/<task_id>")
def delete_task(task_id):
    return delete_record(Task, task_id)


@task_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model_id(Task, task_id) # Does this function specifically need Task imported, since the route_utilities.py has imported Task?

    task.completed_at = datetime.datetime.now()
    db.session.commit()

    notification = send_task_completion_slack(task)

    if notification:
        return {"task": task.to_dict()}, 200


@task_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model_id(Task, task_id)
    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}, 200


# Helper Function

def send_task_completion_slack(task):
    url = "https://slack.com/api/chat.postMessage"
    api_key = os.environ.get("SLACK_BOT_TOKEN")
    header = {"Authorization": f"Bearer {api_key}"}
    request_body = {
        "channel": "C07UJK253A7",
        "text": f"Someone just completed the task {task.title}",
    }

    return requests.post(url, headers=header, params=request_body)