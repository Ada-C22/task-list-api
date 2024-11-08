from flask import Blueprint, request
from app.models.task import Task
from app.db import db
from datetime import date
from .route_utilities import validate_model, create_model, get_models_with_filters
import requests
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task(): 
    request_body = request.get_json()
    return create_model(Task, request_body)

@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_model(Task, task_id)
    return {"task":task.to_dict()}

@tasks_bp.get("")
def get_all_tasks(): 
    return get_models_with_filters(Task, request.args)

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {"task":task.to_dict()}
    return response

@tasks_bp.patch("/<task_id>/mark_complete")
def update_task_complete(task_id):
    task = validate_model(Task, task_id)

    is_complete_check = True

    if task.completed_at is None:
        task.completed_at = date.today() 
        is_complete_check = False
    
    db.session.add(task)
    db.session.commit()

    if not is_complete_check:
        create_slack_msg(task)
        is_complete_check = True 

    response = {"task":task.to_dict()}
    return response

@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    db.session.add(task)
    db.session.commit()

    response = {"task":task.to_dict()}
    return response

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task_id} \"{task.title}\" successfully deleted'}
    return response

def create_slack_msg(task):
    SECRET_KEY_SLACK = os.environ.get("SECRET_KEY_SLACK")

    header = {"Authorization": f"Bearer {SECRET_KEY_SLACK}"}
    data = {
        "channel": "D07GDA3R94P",
        "text": f"Someone just completed the task: {task.title}!"
    }

    return requests.post("https://slack.com/api/chat.postMessage", headers=header, json=data)
