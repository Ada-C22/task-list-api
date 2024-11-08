from flask import Blueprint, abort, make_response, request
from ..db import db
from app.models.task import Task
from datetime import date
import requests 
import os
from app.routes.route_utilities import validate_model, send_slack_message

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        title = request_body["title"]
        description = request_body["description"]
        new_task = Task(title=title, description=description)
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.to_dict()}

    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = db.select(Task).order_by(Task.title.asc())
    elif sort_param == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task).order_by(Task.id)
    
    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]
    return tasks_response


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task" : task.to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {"task": task.to_dict()}

    return response, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    
    db.session.delete(task)
    db.session.commit()

    response = {'details': f'Task {task.id} "{task.title}" successfully deleted'}
    
    return response, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def update_task_mark_completion(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = date.today()
    task.is_complete = True
    db.session.commit()

    send_slack_message(task.title)

    response = {"task": task.to_dict()}
    return response, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_task_mark_incompletion(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    task.is_complete = False
    db.session.commit()

    response = {"task": task.to_dict()}

    return response, 200


    


