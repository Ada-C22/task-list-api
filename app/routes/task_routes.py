from flask import Blueprint,request,abort,make_response,Response
from app.models.task import Task
from ..db import db
from datetime import date
import os
import requests
from .route_utilities import validate_model

tasks_bp = Blueprint("tasks_bp",__name__, url_prefix="/tasks")

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    try:
        new_task = Task.from_dict(request_body)
     
    except KeyError as error:
        response = {"details":f"Invalid data"}
        abort(make_response(response,400))


    db.session.add(new_task)
    db.session.commit()

    response = {"task" : new_task.to_dict()}

    return response,201

@tasks_bp.get("")
def get_all_tasks():
    
    query = db.select(Task)
    sorted_title = request.args.get("sort")
    if sorted_title == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title.asc())
                            
    tasks = db.session.scalars(query)

    tasks_response =([task.to_dict() for task in tasks],200)
    
    return tasks_response

    
@tasks_bp.get("/<task_id>")
def get_single_task(task_id):
    task = validate_model(Task, task_id)

    return {"task" : task.to_dict()}

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task, task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]
    task.completed_at = None
    
    db.session.commit()
    return {"task" : task.to_dict()}

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task, task_id)

    db.session.delete(task)
    db.session.commit()

    return {"details": f'Task {task_id} "{task.title}" successfully deleted'}

@tasks_bp.patch("/<task_id>/mark_complete")
def partial_update_complete_one_task(task_id):
    task = validate_model(Task, task_id)
    
    task.completed_at = date.today()
    
    db.session.add(task)
    db.session.commit()

    message = f"Someone just completed the task My Beautiful {task.title}"
   
    slack_response = requests.post (f"https://slack.com/api/chat.postMessage?channel=C07V6E62DS7&text={message}",headers = {"Authorization":f"Bearer {os.environ.get('SLACK_AUTHENTICATION')}"})
    
   
    return {"task":task.to_dict()}

@tasks_bp.patch("/<task_id>/mark_incomplete")
def partial_update_incomplete_task(task_id):
    task= validate_model(Task, task_id)

    task.completed_at = None

    db.session.add(task)
    db.session.commit()                 
    
    return {"task":task.to_dict()}




    
             
             
