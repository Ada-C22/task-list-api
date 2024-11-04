from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
import json
from app.routes.route_utilities import validate_model
from datetime import datetime
import requests
import os

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    try: 
        new_task = Task.from_dict(request_body)
    except:
        response = {"details":"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title)
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))
    
    query = query.order_by(Task.id)
   
    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
         
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    
    return {"task": task.to_dict()}

@bp.put("/<task_id>")
def update_book(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {"task": task.to_dict()}
    # return Response(response, status=200, mimetype="application/json")
    return response, 200

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}
    # 
    return response, 200

@bp.patch("/<task_id>/mark_complete")
def patch_complete(task_id):
    
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now().isoformat()
    db.session.commit()

    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "channel" : "#task-notifications",
        "text": f"Someone just completed the task {task.title}"
    }

    requests.post(url, headers=headers, json=data)

    response = {"task": task.to_dict()}

    return response, 200

@bp.patch("/<task_id>/mark_incomplete")
def patch_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()

    response = {"task": task.to_dict()}

    return response, 200

