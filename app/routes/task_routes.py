import requests
from flask import Blueprint, abort, make_response, request
from ..db import db
from app.models.task import Task
from datetime import datetime
import os
from dotenv import load_dotenv
from .route_utilities import validate_model

load_dotenv()

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    completed_at = request_body.get("completed_at", None)
            
    new_task = Task.from_dict(request_body)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": new_task.to_dict()
    }
    return response, 201
    
@bp.get("")
def get_all_tasks():
    sort_order = request.args.get('sort')

    if sort_order == 'asc':
        query = db.select(Task).order_by(Task.title.asc())
    elif sort_order == 'desc':
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task).order_by(Task.id)  

    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response, 200

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    task_response = {
        "task": task.to_dict()  
    }

    return task_response, 200

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    if not task:
        abort(make_response({"message": f"task_id {task_id} not found"}, 404))
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body.get("description", task.description)
    task.completed_at = request_body.get("completed_at", task.completed_at)

    db.session.commit()

    response = {
        "task": task.to_dict()  
    }

    return response, 200

@bp.patch("/<task_id>/mark_complete")
def complete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()  
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    slack_token = os.environ.get("SLACK_BOT_TOKEN")
    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }
    request_body = {
        "channel": "C07US894WRL",
        "text": f"Someone just completed the task {task.title}"
    }
    response = requests.post(url, json=request_body, headers=headers)

    if response.status_code == 200:
        return{"task": task.to_dict()}, 200
    else:
        return {"error": "Failed to send Slack notification"}, 500
    

@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None  
    db.session.commit()

    return {"task": task.to_dict()}, 200


@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    if not task:
        abort(make_response({"message": f"task_id {task_id} not found"}, 404))
    
    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }

    return response, 200



