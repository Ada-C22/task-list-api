from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from app.routes.routes_utilities import validate_model
from sqlalchemy import asc, desc
from datetime import datetime
import requests
import os
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    
    try:
        new_task = Task.from_dict(request_body)
    except KeyError as error:
        response_body = {"details": "Invalid data"}
        abort(make_response(response_body, 400))

    db.session.add(new_task)
    db.session.commit()

    response_body = new_task.to_dict()

    return {"task": response_body}, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_params = request.args.get("title")
    if title_params:
        query = query.where(Task.title == title_params)
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.like(f"%{description_param}%"))
    
    sort_params = request.args.get("sort")
    if sort_params == 'asc':
        query = query.order_by(asc(Task.title))
    elif sort_params == 'desc':
        query = query.order_by(desc(Task.title))
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = [task.to_dict() for task in tasks]
    
    return tasks_response, 200

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}, 200


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)

    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']
    db.session.commit()
    
    return {"task": task.to_dict()}, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()
    
    return {"details": f"Task {task.id} \"{task.title}\" successfully deleted"}, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.utcnow()
    task.is_complete = True
    db.session.commit()

    URL = "https://slack.com/api/chat.postMessage"
    
    API_TOKEN = os.getenv('API_TOKEN')
    
    header = {"Authorization": f"Bearer {API_TOKEN}"}
    response_body = {
        "channel": "C080163FK25",
        "text": f"Someone just completed the task {task.title}"
    }
    response = requests.post(URL, json=response_body, headers=header)
    if response.status_code != 200:
       return {"msg": "Failure to send message"}
    
    return {"task": task.to_dict()}, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = None
    task.is_complete = False
    db.session.commit()

    return {"task": task.to_dict()}, 200


