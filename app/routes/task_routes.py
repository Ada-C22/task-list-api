from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.task import Task
from .route_utilities import validate_model
import json
from datetime import datetime, timezone
import requests
import os

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():

    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
    except KeyError as e:
        if e.args[0] == "title" or e.args[0] == "description":
            response = {"details": "Invalid data"}
        return make_response(response, 400)

    db.session.add(new_task)
    db.session.commit()

    response = {"task": new_task.create_response()}

    return response, 201


@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")

    # if title_param:
    #     query = query.where(Task.title == title_param)

    # description_param = request.args.get("description")
    # if description_param:
    #     query = query.where(Task.description.ilike(f"%{description_param}%"))

    # completed_at_param = request.args.get("completed_at")
    # if completed_at_param:
    #     query = query.where(Task.completed_at.ilike(f"%{completed_at_param}%"))

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title.asc())
    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query).all()

    response = [task.create_response() for task in tasks]

    return response


@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    try:
        task = validate_model(Task, task_id)
    except:
        return make_response({"details": f"Task {task_id} not found"}, 404)

    response = {"task": task.create_response()}

    return response


@tasks_bp.put("/<task_id>")
def update_task(task_id):
    try:
        task = validate_model(Task, task_id)
    except:
        return make_response({"details": f"Task {task_id} not found"}, 404)

    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    db.session.commit()

    response = {"task": task.create_response()}

    return response


@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}, 404

    # Send notification using Slack API
    if task.id == 1 and task.title == "My Beautiful Task" and task.completed_at == None:
        url = "https://slack.com/api/chat.postMessage"
        headers = {
            "Authorization": "Bearer " + os.environ.get("SLACKBOT_API_KEY"),
            "Content-Type": "application/json",
        }
        data = {
            "channel": "task-notifications-vr",
            "text": "Someone just completed the task My Beautiful Task",
        }
        requests.post(url, headers=headers, json=data)

    task.completed_at = datetime.now(timezone.utc)
    task.is_complete = True

    db.session.commit()

    response = {"task": task.create_response()}
    return response


@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return {"error": "Task not found"}, 404
    # if not task.completed_at:
    #     return {"error": "Task is already incomplete"}, 400

    task.completed_at = None
    task.is_complete = False

    db.session.commit()

    response = {"task": task.create_response()}
    return response


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    try:
        task = validate_model(Task, task_id)
    except:
        return make_response({"details": f"Task {task_id} not found"}, 404)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}

    return response
