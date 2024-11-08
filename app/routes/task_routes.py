from flask import Blueprint, abort, make_response, request, Response, jsonify
from app.models.task import Task
from ..db import db
from datetime import datetime
import os
from dotenv import load_dotenv
import requests
from app.routes.route_utilities import validate_model, check_complete

load_dotenv()
SLACKBOT_TOKEN = os.getenv("SLACKBOT_TOKEN")

tasks_bp = Blueprint("task_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():

    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    if "description" not in request_body:
        return {"details": "Invalid data"}, 400

    if "completed_at" in request_body:
        completed_at = request_body["completed_at"]

    else:
        completed_at = None

    new_task = Task(title=request_body["title"], description=request_body["description"], completed_at=completed_at )
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task": {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": check_complete(new_task.completed_at)

    }
    }

    return response, 201

@tasks_bp.get("")
def get_all_tasks():

    query = db.select(Task)

    title_param = request.args.get("title")
    if title_param:
        query = db.select(Task).where(Task.name == title_param)
        
    sort_param = request.args.get("sort")
    if sort_param == "desc":
        query = query.order_by(Task.title.desc())

    else:
        query = query.order_by(Task.title.asc())

    tasks = db.session.scalars(query)
    
    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {             
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": check_complete(task.completed_at)
                
            }
        )

    return tasks_response

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task, task_id)
    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if task.goal_id:
        return {
                "task": task.to_dict()
                
            }
    else:
        return {
                    "task": {
                        "id": task.id,
                        "title": task.title,
                        "description": task.description,
                        "is_complete": check_complete(task.completed_at)
                    }
                }

    

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body['title']
    task.description = request_body['description']

    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]

    else:
        task.completed_at = None

    db.session.commit()

    return {
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": check_complete(task.completed_at)
                }
            }

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details": f"Task {task_id} \"Go on my daily walk 🏞\" successfully deleted"}

# @tasks_bp.patch("/<task_id>/mark_complete")
# def task_mark_complete(task_id):
#     task = validate_task(task_id)
    
#     task.completed_at = datetime.now()

#     db.session.commit()

#     return {
#                 "task": {
#                     "id": task.id,
#                     "title": task.title,
#                     "description": task.description,
#                     "is_complete": check_complete(task.completed_at)
#                 }
#             }

@tasks_bp.patch("/<task_id>/mark_incomplete")
def task_mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = None

    db.session.commit()

    return {
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "is_complete": check_complete(task.completed_at)
                }
            }

@tasks_bp.patch("/<task_id>/mark_complete")
def task_mark_complete_slack(task_id):
    task = validate_model(Task, task_id)

    task.completed_at = datetime.now()
    db.session.commit()

    slack_message = {
        "channel": "task-notifications",
        "text": f"Someone just completed the task {task.title}"

    }

    # Send the Slack message
    headers = {"Authorization": f"Bearer {SLACKBOT_TOKEN}"}
    slack_response = requests.post(
        "https://slack.com/api/chat.postMessage",
        json=slack_message,
        headers=headers
    )

    # Check Slack response for success
    if slack_response.status_code != 200 or not slack_response.json().get("ok"):
        return jsonify({"message": "Failed to send Slack notification"}), 500

    # Return response if successful
    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": check_complete(task.completed_at)
        }
    }, 200

















