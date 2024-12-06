from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from ..db import db
from datetime import datetime
from app.models.task import Task

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")



@tasks_bp.post("")
def create_task():
  request_body = request.get_json()

  try:
     new_task = Task.from_dict(request_body)

  except KeyError:
     response = {"details": "Invalid data"}
     abort(make_response(response, 400))


  db.session.add(new_task)
  db.session.commit()

  response = {"task": new_task.to_dict()}
  return response, 201


@tasks_bp.get("")
def get_all_tasks():
  query = db.select(Task)
  description_param = request.args.get("description")
  if description_param:
    query = query.where(Task.description.ilike(f"%{description_param}%")).order_by(Task.id)

  title_param = request.args.get("title")
  sort = request.args.get("sort", "asc")  # Default to ascending order

  query = db.select(Task)

  if title_param:
      query = query.where(Task.title.ilike(f"%{title_param}%"))

  if sort == "desc":
      query = query.order_by(Task.title.desc())
  else:
      query = query.order_by(Task.title.asc())

  tasks = db.session.scalars(query)
  tasks_response = [task.to_dict() for task in tasks]

  return tasks_response, 200


@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
  task = validate_task(task_id)


  return {"task": task.to_dict()}


@tasks_bp.put("/<task_id>")
def update_task(task_id):
  task = validate_task(task_id)
  request_body = request.get_json()

  task.title = request_body["title"]
  task.description = request_body.get("description")
  task.completed_at = request_body.get("completed_at")

  db.session.commit()
  response = {"task": task.to_dict()}
  return response, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_task(task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    return {"task": task.to_dict()}, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_task(task_id)
    task.completed_at = None

    db.session.commit()

    return {"task": task.to_dict()}, 200


@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
  task = validate_task(task_id)

  db.session.delete(task)
  db.session.commit()
  response = {
    "details": f'Task {task_id} "{task.title}" successfully deleted'
    }
  return response, 200

def validate_task(task_id):
  try:
      task_id = int(task_id)
  except ValueError:
        response = {"details": f"Task {task_id} invalid"}
        abort(make_response(response, 404))

  task = db.session.get(Task,task_id)

  if not task:
        response = {"message": f"task {task_id} not found"}
        abort(make_response(response, 404))

  return task