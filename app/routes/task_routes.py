from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model
from datetime import datetime
import requests
import os

bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()
    try: 
        new_task = Task.from_dict(request_body)

    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return {"task": new_task.to_dict()}, 201 

@bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))

    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    sort_param = request.args.get("sort", "asc")
    if sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title.asc())
    
    query = query.order_by(Task.id)
    tasks = db.session.execute(query).scalars().all()

    tasks_response = [task.to_dict() for task in tasks]
    
    return tasks_response

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)

    return {"task": task.to_dict()}, 200 

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    return {"task": task.to_dict()}, 200 

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return {
        "details": f'Task {task_id} "{task.title}" successfully deleted'
    }, 200

@bp.patch("/<task_id>/mark_complete")
def mark_complete_on_incomplete_task(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.add(task)
    db.session.commit()
    
    send_to_slack(task)
    return {"task": task.to_dict()}, 200 

def send_to_slack(task):

    headers = {
        "Authorization": os.environ.get("SLACK_BOT_TOKEN")
    }
    request_body = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}.",
    }
    requests.post("https://slack.com/api/chat.postMessage", headers=headers, data=request_body)



@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete_on_complete_task(task_id):
    task = validate_model(Task, task_id)

    if task.completed_at:
        task.completed_at = None 
    db.session.add(task)
    db.session.commit()

    return { "task": task.to_dict()}, 200

