from flask import Blueprint, request, Response, make_response, abort
from app.models.task import Task
from ..db import db
from datetime import datetime
import os
import requests
from os import environ


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks" )

@bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)

    except KeyError as e:
        print(e)
        response = {
            "details": "Invalid data"
        }
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

    completed_at_param = request.args.get("completed_at")
    if completed_at_param:
        query = query.where(Task.completed_at.ilike(f"%{completed_at_param}%"))

    sort_param = request.args.get("sort")
    if sort_param:
        if sort_param == "asc":
            query = query.order_by(Task.title.asc())
        elif sort_param == "desc":
            query = query.order_by(Task.title.desc())

    query = query.order_by(Task.id)
    tasks = db.session.scalars(query)
    
    response = [task.to_dict() for task in tasks]
    return response, 200

@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {"task": task.to_dict()}


@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {
        "task": task.to_dict()
    }

    return response, 200

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_task(task_id)

    task.completed_at = datetime.utcnow()
    db.session.commit()

    if os.environ.get('SEND_SLACK_NOTIFICATIONS') == "True":
        send_slack_notification(task.title)

    response = {
        "task": task.to_dict()
    }

    return response, 200

def send_slack_notification(task_title):
    request_data = {
        "channel": "#api-test-channel",
        "username": "LD bot",
        "text": f"Someone just completed the task \"{task_title}\""
    }

    response = requests.post(
        url="https://slack.com/api/chat.postMessage",
        json=request_data,
        headers={"Authorization": f"Bearer {environ.get('SLACK_WEB_CLIENT_TOKEN')}"},
        timeout=5
    )
    response.raise_for_status()
    return response.json().get("ok", False)

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_task(task_id)

    if task.completed_at != None:
        task.completed_at = None
        db.session.commit()
    else:
        pass

    response = {
        "task": task.to_dict()
    }

    return response, 200

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }

    return response, 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"details": "Invalid data"}

        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)
    
    if not task:
        response = {"message": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task
