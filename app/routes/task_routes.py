from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from datetime import datetime
from ..db import db
import requests
import os


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()
    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    if "description" not in request_body:
        return {"details": "Invalid data"}, 400

    title = request_body["title"]
    description = request_body["description"]
    completed_at= request_body.get("completed_at")

    new_task = Task(title=title, description=description, completed_at= None if completed_at is None else datetime.datetime(completed_at)
    )
    db.session.add(new_task)
    db.session.commit()

    
    response = { "task" : {
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "is_complete": new_task.completed_at is not None 
    }
    }
    return response, 201

@tasks_bp.get("")
def get_all_tasks():
    sort_order = request.args.get("sort")

    if sort_order == "asc":
        query = db.select(Task).order_by(Task.title.asc())
    elif sort_order == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task).order_by(Task.id)

    tasks = db.session.scalars(query)

    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                # "goal_id": task.goal_id is not None,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            }
        )
    return tasks_response, 200

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id)

    if task.goal_id is not None:
        return {
            "task": {
                "id": task.id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            }
        }
    else:
        return {
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            }
        }

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

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at= request_body.get("completed_at")
    # task.goal_id= request_body.get("goal_id")
    db.session.commit()


    response = { "task" : {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    }
    }
    return response, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    
    db.session.delete(task)
    db.session.commit()

    response = {
        "details": f"Task {task.id} \"{task.title}\" successfully deleted"
    }
    
    return response, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def update_task_to_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()
    token = os.environ.get('SLACK_API_TOKEN')
    headers = {
        "Authorization": f"Bearer {token}" 
    }
    url = "https://slack.com/api/chat.postMessage"

    message = {"channel": "D07V10LPBM4",
            "text": f"Someone just completed the task {task.title}"}

    response = requests.post(url, headers=headers, data=message)
    
    print(response.text)
    response = { "task": {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    }
    }
    return response, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def update_task_to_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None
    db.session.commit()

    response_body = { "task": {
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    }
    }
    return response_body, 200
