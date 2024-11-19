from flask import Blueprint, abort, make_response, request, Response, jsonify
from app.models.task import Task
from sqlalchemy import desc
from datetime import datetime
from ..db import db
import os
import requests

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        response = {"details": "Invalid data"}
        return make_response(response, 400)

    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at", None)


    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at) 
        }
    }

    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Task.title.ilike(f"%{title_param}%"))
    
    description_param = request.args.get("description")
    if description_param:
        query = query.where(Task.description.ilike(f"%{description_param}%"))

    completed_at_param = request.args.get("completed_at")
    if completed_at_param == "true":
        query = query.where(Task.completed_at.isnot(None))
    elif completed_at_param == "false":
        query = query.where(Task.completed_at.is_(None))

    sort_param = request.args.get("sort")
    if sort_param == "asc":
        query = query.order_by(Task.title)
    if sort_param == "desc":
        query = query.order_by(desc(Task.title))
    else:
        query = query.order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append({
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        })
    
    return tasks_response, 200

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task":task.to_dict()
        }, 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))
    return task

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)
    task.completed_at = request_body.get("completed_at", task.completed_at)
    db.session.commit()

    return {
        "task":task.to_dict()
        }, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    if not task:
        return jsonify({"message": f"task {task_id} not found"}), 404
    db.session.delete(task)
    db.session.commit()

    return jsonify({
        "details": f'Task {task.id} "{task.title}" successfully deleted'
    }), 200


def mark_task_complete(task_id):
    task = validate_task(task_id)
    if not task:
        return abort(404, description="Task not found")
    
    task.completed_at = datetime.now()
    db.session.commit()

    return {
        "task":task.to_dict()
        }, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def patch_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now().isoformat()
    db.session.commit()
    
    url = "https://slack.com/api/chat.postMessage"
    headers = {
        "Authorization": f"Bearer {os.environ.get('SLACK_API_KEY')}",
        "Content-Type": "application/json"
    }
    data = {
        "channel" : "#api-test-channel",
        "text": f"Someone just completed the task {task.title}"
    }

    response = requests.post(url, headers=headers, json=data)

    print("Slack API Response:", response.status_code, response.json())

    response_data = {"task": task.to_dict()}

    return response_data, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    if not task:
        return abort(404, description="Task not found")

    task.completed_at = None
    db.session.commit()

    return {
        "task":task.to_dict()
        }, 200

