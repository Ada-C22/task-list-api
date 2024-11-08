from flask import Blueprint, request, jsonify, make_response, abort
from app.models.task import Task
from ..db import db
from datetime import datetime
from app.slack_service import send_slack_message


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

def validate_task(task_id):
    try:
        task_id = int(task_id)
    except:
        abort(make_response({"message": f"Task {task_id} not found"}, 400))

    task = Task.query.get(task_id)
    if not task:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))
    return task

# POST: Create a new task
@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))

    new_task = Task(
        title=request_body["title"],
        description=request_body["description"], 
        completed_at=None
    )
    db.session.add(new_task)
    db.session.commit()
    
    return make_response({
        "task": {
            "id": new_task.id,
            "title": new_task.title,
            "description": new_task.description,
            "is_complete": False
        }
    }, 201)

# GET all tasks
@tasks_bp.get("")
def get_all_tasks():
    # Start the base query without resetting it
    query = db.select(Task)
    sort_order = request.args.get("sort", "asc")
    if sort_order == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title.asc())

    # Execute the query
    tasks = db.session.scalars(query)

    # Build the response
    tasks_response = [{
        "id": task.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    } for task in tasks]

    return jsonify(tasks_response), 200

# GET one task
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task(task_id) 

    return {
        "task": task.task_dict()
    }, 200


# PUT: Update an existing task
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    request_body = request.get_json()

    if "title" not in request_body or "description" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))


    task.title = request_body.get("title", task.title)
    task.description = request_body.get("description", task.description)

    db.session.commit()

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }, 200

# PATCH: Partial update tasks
@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    # task.title = request.json.get("title", task.title)
    task.completed_at = datetime.now().date()
    db.session.commit()

    send_slack_message(task.title)

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = db.session.get(Task, task_id)

    if task is None:
        abort(make_response({"message": f"Task {task_id} not found"}, 404))

    task.completed_at = None
    db.session.commit()

    return {
        "task": {
            "id": task.id,
            "title": task.title,
            "description": task.description,
            "is_complete": task.completed_at is not None
        }
    }, 200

# DELETE: Delete a task
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task(task_id)

    db.session.delete(task)
    db.session.commit()

    return make_response({
        "details": f"Task {task_id} \"{task.title}\" successfully deleted"
    }, 200)
    

    
