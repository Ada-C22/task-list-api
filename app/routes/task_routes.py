from flask import Blueprint, abort, make_response, request
from ..models.task import Task
from ..db import db
from datetime import datetime, timezone
from .routes_utilities import validate_model, create_model, get_models_with_filters
import os
import requests


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
SLACK_TOKEN = os.environ.get("SLACK_TOKEN")

@tasks_bp.post("")
def create_task():
    response_body = request.get_json()

    if not response_body.get("title") or not response_body.get("description"):
        abort(make_response({"details": "Invalid data"}, 400))

    return {
        "task": create_model(Task, response_body)
        }, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}"))

    sort_order = request.args.get('sort', 'asc')
    if sort_order == 'asc':
        query = query.order_by(Task.title.asc())
    elif sort_order == 'desc':
        query = query.order_by(Task.title.desc())
    
    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    task_response = {
        "task": task.to_dict()
        }
    return task_response

@tasks_bp.put("/<task_id>")
def update_one_task(task_id):
    task = validate_model(Task, task_id)
    response_body = request.get_json()

    task.title = response_body.get("title")
    task.description = response_body.get("description")
    db.session.commit()

    task_response = {
        "task": task.to_dict()
    }
    return task_response, 200

@tasks_bp.delete("/<task_id>")
def delete_one_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
        }

@tasks_bp.patch("/<task_id>/mark_complete")
def task_complete(task_id):
    try:
        task = validate_model(Task, task_id)
    except ValueError:
        abort(make_response({"message": f"Task with {task_id} is invalid"}, 400))

    task.is_complete = True
    task.completed_at = str(datetime.now(timezone.utc))

    db.session.add(task)
    db.session.commit()

    #Slack bot addition
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f'Bearer {SLACK_TOKEN}'
        }
    payload = {
        "channel": "C0804BP04NL",
        "text": f"Someone just completed the task {task.title}"
    }
    slack_response = requests.post(url, json=payload, headers=headers)

    task_response = {
        "task": task.to_dict()
    }
    return task_response, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.is_complete = False
    task.completed_at = None

    db.session.add(task)
    db.session.commit()

    task_response = {
        "task": task.to_dict()
    }
    return task_response, 200