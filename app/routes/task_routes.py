from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.routes.utilities_routes import create_model, validate_model, get_models_with_filters, delete_model
from app.routes.slack_functions import send_message_with_config
from datetime import datetime, timezone
from ..db import db
import os


bp = Blueprint("task_bp", __name__, url_prefix="/tasks")
invalid_data_response = ({"details": "Invalid data"}, 400)

#create a new task in database
@bp.post("")
def create_task(): 
    request_body = request.get_json()
    return create_model(Task, request_body)

@bp.get("")
def get_tasks(): 
    request_arguments = request.args
    return get_models_with_filters(Task, request_arguments), 200


#get task by task id: 
@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    task_dict = task.to_dict()
    response = {"task":task_dict}

    return response,200

#update task
@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    
    request_body = request.get_json()
    title = request_body.get("title")
    description = request_body.get("description")

    if not title or not description: 
        return {"error": "Missing required fields: 'title' or 'description'"}, 400
    task.title = title 
    task.description = description 

    completed_at = request_body.get("completed_at", task.completed_at)
    task.completed_at = completed_at

    db.session.commit()
    
    response = {"task":task.to_dict()}
    return response, 200


#Delete task
@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    return delete_model(Task, task)


#route 2
@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)

    utc_now = datetime.now(timezone.utc)
    task.completed_at = utc_now
    message = f"Task {task.title} has been marked as complete!"
    slack_response= send_message_with_config(message)
    db.session.commit()
    response = {"task": task.to_dict()}
    if slack_response == None:
    # if slack_response.status_code != 200 or not slack_response.json().get("ok"): 
        # error_msg = slack_response.json().get("errror", "Unknown error")
        print("slack_error : Failed to send slack Notification")

    return response, 200 


@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    response = {"task": task.to_dict()}
    return make_response(response,200)


