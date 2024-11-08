from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from app.db import db
from datetime import datetime
import os
import requests
from app.routes.route_utilities import validate_model

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        return {"details": "Invalid data"}, 400

    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at", None)
    is_complete = request_body.get("is_complete", False)
    goal_id = request_body.get("goal_id", None)

    new_task = Task(
        title=title,
        description=description,
        is_complete=is_complete,
        goal_id=goal_id
    )
    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_dict()}
    return response, 201


@tasks_bp.get("")
def get_all_tasks():
    
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        query = db.select(Task).order_by(Task.title.asc())
    elif sort_order == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task).order_by(Task.id)
    
    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict(include_goal_id=True) for task in tasks]

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_model(Task, task_id)

    include_goal_id = task.goal_id is not None
    return {"task": task.to_dict(include_goal_id=include_goal_id)}


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at", None)
    task.is_complete = request_body.get("is_complete", False)

    db.session.commit()

    return {"task": task.to_dict()}


@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    api_key = os.environ.get("SLACK_BOT_TOKEN")
    headers = {"Authorization": f"Bearer {api_key}"}
    request_body = {
        "channel": "task-notifications",
        "text": f"Task '{task.title}' has been completed!"
    }

    response = requests.post(url, headers=headers, data=request_body)

    if response.status_code != 200:
        return {"error": "Failed to send Slack notification"}, 500
    
    return {"task": task.to_dict()}, 200


@tasks_bp.patch("<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "Go on my daily walk 🏞" successfully deleted'}
