from flask import Blueprint, abort, make_response, Response, request
from .route_utilities import validate_model, create_model, get_models_with_filters, post_slack_message
from app.db import db
from app.models.task import Task
from datetime import datetime


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.get("")
def get_all_tasks():
    return get_models_with_filters(Task, request.args)


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    return create_model(Task, request_body)


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    response_body = {"task": task.to_dict()}
    
    return response_body


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()
    task.title = request_body.get("title")
    task.description = request_body.get("description")
    db.session.commit()

    response_body = {"task": task.to_dict()}

    return make_response(response_body, 200)


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)  
    db.session.delete(task)
    db.session.commit()

    response_body = {
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }
    return make_response(response_body, 200)


@tasks_bp.patch("/<task_id>/mark_complete")
def update_mark_complete_task(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()

    db.session.commit()

    post_slack_message(task)

    response_body = {"task": task.to_dict()}

    return make_response(response_body, 200)


@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_mark_incomplete_task(task_id):
    task = validate_model(Task, task_id) 

    task.completed_at = None
    db.session.commit()

    response_body = {"task": task.to_dict()}
    return make_response(response_body, 200)