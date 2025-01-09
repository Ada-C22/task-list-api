import os
import requests
from flask import Blueprint, abort, make_response, request, Response
from datetime import datetime, timezone
from app.models.task import Task
from ..db import db
from dotenv import load_dotenv
from app.models.goal import Goal

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_tasks():
    sort_order = request.args.get("sort", "asc").lower()  # Default to ascending
    
    if sort_order == "desc":
        tasks = Task.query.order_by(Task.title.desc()).all()  
    else:
        tasks = Task.query.order_by(Task.title.asc()).all()  

    # Prepare response data
    task_list = [
        {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
        for task in tasks
    ]

    return (task_list), 200

@tasks_bp.get("/<int:task_id>")
def get_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    return {"task": {
        "id": task.id,
        "goal_id": task.goal_id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    }}, 200

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    title = request_body.get("title")
    description = request_body.get("description")
    completed_at = request_body.get("completed_at")  

    if not title or not description:
        return {"details": "Invalid data"}, 400

    if completed_at is None:
        completed_at = None

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    return {"task": {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at is not None
    }}, 201

@tasks_bp.put("/<int:task_id>")
def update_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")
    completed_at = request_body.get("completed_at") 

    # Update attributes if provided in request body
    if title:
        task.title = title
    if description:
        task.description = description
    if completed_at is not None:  
        task.completed_at = completed_at

    db.session.commit()

    return {"task": {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    }}, 200

@tasks_bp.delete("/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    db.session.delete(task)
    db.session.commit()
    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}, 200

@tasks_bp.patch("/<int:task_id>/mark_complete")
def task_complete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    task.completed_at = datetime.now()
    db.session.commit()

    slack_token = os.environ.get('SLACK_TOKEN')
    slack_url = "https://slack.com/api/chat.postMessage"
    slack_data = {
        "channel": "api-test-channel", 
        "text": "Someone just completed the task " + task.title
    }
    slack_header = {
        "Authorization": f"Bearer {slack_token}",
    }

    requests.post(slack_url, data=slack_data, headers=slack_header)

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": True
        }
    }, 200

@tasks_bp.patch("/<int:task_id>/mark_incomplete")
def task_incomplete(task_id):
    task = Task.query.get(task_id)

    if not task:
        return {"message": f"Task {task_id} not found"}, 404

    task.completed_at = None
    db.session.commit()

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": False
        }
    }, 200