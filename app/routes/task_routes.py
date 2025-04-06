from flask import Blueprint, request, abort, make_response, Response
import requests
import os
from ..db import db
from app.models.task import Task
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()


bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json()

    # Check for missing fields
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    new_task = Task.from_dict(request_body)

    db.session.add(new_task)
    db.session.commit()

    # Return the response with the new task's dictionary format
    return make_response({"task": new_task.to_dict()}, 201)

@bp.get("")
def get_all_tasks():
    
    sort_order = request.args.get("sort")  # Get the sort parameter from the query string
    tasks = Task.query.all()  # Get all tasks from the database

    # Sort tasks based on the sort_order
    if sort_order == "asc":  
        tasks.sort(key=lambda task: task.title)
    elif sort_order == "desc":
        tasks.sort(key=lambda task: task.title, reverse=True)

    # Convert each task to a dictionary
    tasks_response = [task.to_dict() for task in tasks]
    
    return make_response(tasks_response, 200)


    

@bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_task(task_id)

    return make_response({"task": task.to_dict()}, 200)

@bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = request_body.get("completed_at")


    db.session.commit()

    return make_response({"task": task.to_dict()}, 200)

@bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({"details": f'Task {task.id} "{task.title}" successfully deleted'}, 200)

@bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    # Retrieve the task by ID
    task = validate_task(task_id)
    
    # If the task is not found, return a 404 error
    if task is None:
        abort(404, description="Task not found")
    
    # Update task to mark it as complete
    task.completed_at = datetime.now(timezone.utc)  # set to current UTC time
    db.session.commit()

    # Send notification to Slack
    slack_message = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task: {task.title}"
    }

    slack_url = "https://slack.com/api/chat.postMessage"
    slack_headers = {
        "Authorization": f"Bearer {os.environ.get('SLACKBOT_TOKEN')}",
        "Content-Type": "application/json"
    }

    response = requests.post(slack_url, json=slack_message, headers=slack_headers)

    if response.status_code != 200:
        print(f"Error sending message to Slack: {response.text}")

    return {"task": task.to_dict()}, 200

@bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    # Use validate_task to handle 404 if the task does not exist
    task = validate_task(task_id)

    task.completed_at = None
    db.session.commit()

    return {"task": task.to_dict()}, 200

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        abort(make_response({"message": f"Task id '{task_id}' is invalid"}, 400))

    task = db.session.query(Task).filter_by(id=task_id).first()

    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    return task







