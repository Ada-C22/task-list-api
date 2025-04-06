from flask import Blueprint, abort, jsonify, make_response, request
from ..db import db
from ..models.task import Task
from datetime import datetime
# from .route_utilities import validate_model, create_model, validate_task
import os
import requests

TOKEN = os.environ.get("SLACK_TOKEN")
SLACK_CHANNEL=os.environ.get("SLACK_CHANNEL")
bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@bp.post("")
def create_task():
    
    try:
        request_body = request.get_json()
        title = request_body["title"]
        description = request_body["description"]
        new_task = Task(title=title, description=description)

        db.session.add(new_task)
        db.session.commit()

        return new_task.to_dict(), 201
    
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))



def send_slack_msg(task_title):
    """
    Information obtained from Slack Wep API Docmentation:
    https://api.slack.com/methods/chat.postMessage
    """
    
    url=os.environ.get("SLACK_URL")
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {TOKEN}"
    }

    data={
        "channel": SLACK_CHANNEL,
        "text": f"Someone just completed the task: {task_title}"
    }

    requests.post(url, headers=headers, json=data)
    
    
@bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):

    current_task = validate_task(task_id)

    if not current_task.completed_at:
        current_task.completed_at = datetime.now()

    send_slack_msg(current_task.title)

    db.session.add(current_task)
    db.session.commit()

    response = current_task.to_dict()

    return jsonify(response)




@bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):

    current_task = validate_task(task_id)

    if current_task.completed_at:
        current_task.completed_at = None

    db.session.add(current_task)
    db.session.commit()

    response = {"task": current_task.to_dict()}

    return jsonify(response)


@bp.get("")
def get_tasks_sort_title():

    query = db.select(Task)

    title_sort = request.args.get("sort")
    if title_sort and title_sort == "asc":
        query = query.order_by(Task.title)
    
    elif title_sort and title_sort == "desc":
        query = query.order_by(Task.title.desc())

    tasks = db.session.scalars(query)
    tasks_response = [task.to_dict() for task in tasks]

    return jsonify(tasks_response)


@bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)
    response = {"task": task.to_nested_dict()}
    return response



@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    db.session.commit()

    return {"task": task.to_dict()} 

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    response = {"details": f'Task {task_id} "{task.title}" successfully deleted'}

    return jsonify(response)


def validate_task(task_id):
    try:
        task_id = int(task_id)
    
    except:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"details": f"Task {task_id} not found"}
        abort(make_response(response, 404))

    return task

# 


    
