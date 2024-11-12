from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime, timezone

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")


@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    #validate request data
    if "title" not in request_body or "description" not in request_body:
        response = {"details": "Invalid data"}
        return make_response(response,400)

    title = request_body["title"]
    description = request_body["description"]
    completed_at = request_body.get("completed_at")

    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task":{
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": bool(new_task.completed_at)
        }
    }
    return response, 201

@tasks_bp.get('/<task_id>')
def get_one_task(task_id):
    task = validate_task(task_id)

    return {
        "task":{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": bool(task.completed_at)
        }
    }

@tasks_bp.get("")
def get_all_tasks():

    sort_param = request.args.get("sort", "").lower()
    
    if sort_param and sort_param.lower() == "asc":
        query = db.select(Task).order_by(Task.title)

    elif sort_param and sort_param.lower() == "desc":
        query = db.select(Task).order_by(Task.title.desc())
    else:
        query = db.select(Task).order_by(Task.title)

    tasks = db.session.scalars(query)


    tasks_response = []
    for task in tasks:
        tasks_response.append(
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)
            }
        )
    return tasks_response

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task(task_id)
    request_body = request.get_json()

    # Validate request data
    if "title" not in request_body or "description" not in request_body:
        return make_response({"details": "Invalid data"}, 400)

    task.title = request_body["title"]
    task.description = request_body["description"]
    
    # Keep completed_at unchanged if not provided
    if "completed_at" in request_body:
        task.completed_at = request_body["completed_at"]
    
    db.session.commit()

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)  # Convert completed_at to boolean
        }
    }, 200
    
@tasks_bp.delete("<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)
    db.session.delete(task)
    db.session.commit()

    return {"details":f'Task {task_id} "{task.title}" successfully deleted'},200 
    # Response(status=204, mimetype="application/json")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except ValueError:
        response = {"message": f"task {task_id} invalid"}
        abort(make_response(response,400))

    query = db.select(Task).where(Task.id == task_id)
    task = db.session.scalar(query)

    if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

    return task

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_task(task_id)
    
    # Update completed_at to mark the task as completed
    task.completed_at = datetime.now(timezone.utc)
    
    # Commit the changes to the database
    db.session.commit()

    # Prepare the response
    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }
    return response, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_task(task_id)
    
    # Update completed_at to mark the task as completed
    task.completed_at = None
    
    # Commit the changes to the database
    db.session.commit()

    # Prepare the response
    response = {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": bool(task.completed_at)
        }
    }
    return response, 200




