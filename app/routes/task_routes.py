from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.routes.utilities_routes import create_model, validate_model, get_models_with_filters, check_for_completion, delete_model
from ..db import db
from datetime import datetime
import requests


tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")
invalid_data_response = ({"details" : "Invalid data"}, 400)

#create a new task in database
@tasks_bp.post("")
def create_task(): 
    request_body = request.get_json()
    return create_model(Task,request_body)

@tasks_bp.get("")
def get_tasks():
    query = db.select(Task)
    title_param = request.args.get("title")
    if title_param: 
        query = query.where(Task.title.ilike(f"%{title_param}%"))
        title_param = request.args.get("title")
    
    description_param = request.args.get("description")
    if description_param: 
        query = query.where(Task.description.ilike(f"%{description_param}%"))


    is_complete_param = request.args.get("is_complete")
    if is_complete_param: 
        query = query.where(Task.is_complete.ilike(f"%{is_complete_param}%"))
    

    sort_param = request.args.get("sort")
    if sort_param == "asc": 
        query = query.order_by(Task.title.asc())

    elif sort_param == "desc":
        query = query.order_by(Task.title.desc())
    
    tasks = db.session.scalars(query)

    tasks_response = []

    for task in tasks:  
        tasks_response.append(task.to_dict())

    return tasks_response,200
    

#get task by task id: 
@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_model(Task,task_id)
    task_dict = task.to_dict()
    response = {"task":task_dict}
    expected = {
        "task": {
            "id": 1,
            "title": "A Brand New Task",
            "description": "Test Description",
            "is_complete": False
        }
    }
    print("the task dictionary is:\n", dict)
    print("the expected dictitonary was:\n",expected) 
    return response,200

#update task
@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_model(Task,task_id)
    
    request_body = request.get_json()
    task.title = request_body["title"]
    task.description = request_body["description"]
    try:
        completed_at = request_body["completed_at"]
    except:
        completed_at=task.completed_at
    
    task.completed_at = completed_at
    db.session.commit()
    
    response = {"task":task.to_dict()}
    return response, 200


#Delete task
@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_model(Task,task_id)
    return delete_model(Task, task)
    # task_title = task.title

    # db.session.delete(task)
    # db.session.commit()
    # details = f"Task {task_id} \"{task_title}\" successfully deleted"
    # response_body = {"details" : details}

    # return response_body


#route 2
@tasks_bp.patch("/<task_id>/mark_complete")
def mark_complete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = datetime.now()
    db.session.commit()

    message = f"Task {task.title} has been marked as complete!"
    
    slack_url = "http://127.0.0.1:5000/send_message"
    payload = {
        "message": message,
        "channel": "api-test-channel"
    }

    try:
        response = requests.post(slack_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"failed to send slack message: {e}")

    response = {"task": task.to_dict()}
    return make_response(response, 200)

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_incomplete(task_id):
    task = validate_model(Task, task_id)
    task.completed_at = None
    db.session.commit()
    response = {"task": task.to_dict()}
    return make_response(response,200)



#helperfunctions
    



