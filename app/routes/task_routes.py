from flask import Blueprint, request, abort, make_response, Response
from app.models.task import Task
from datetime import datetime
from app.routes.route_utilities import validate_model
from ..db import db
from app.routes.route_utilities import send_slack_message

bp = Blueprint("task_bp", __name__,url_prefix="/tasks")

@bp.post("")
def create_task():
    request_body = request.get_json() 

    try:
        new_task = Task.from_dict(request_body)
    except:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    db.session.add(new_task)
    db.session.commit()

    return new_task.to_dict(), 201

@bp.get("")
def get_all_tasks():

    query = db.select(Task) #select records from db Model

    # Check for sorting parameter and apply
    sorting_param = request.args.get("sort", "asc")
    
    if sorting_param == "desc":
        query = query.order_by(Task.title.desc())
    else:
        query = query.order_by(Task.title)

    #query = query.order_by(Task.id)#select records
    tasks = db.session.scalars(query) #retrieve the records
    
    response =[]
    for task in tasks:
        response.append(task.to_dict(include_name=False))
    return response 

@bp.get("/<task_id>")
def get_one_task_by_id(task_id):

    task = validate_model(Task,task_id)

    if task.goal_id:
        return task.to_dict(goal_id=True)
    else:
        return task.to_dict()

@bp.put("/<task_id>")
def update_one_task_by_id(task_id):

    task = validate_model(Task,task_id) #record with id = task_id
    request_body = request.get_json()
    
    #Update the task
    task.title = request_body["title"]
    task.description = request_body["description"]

    db.session.commit() #save the changes to db

    return task.to_dict()

@bp.patch("/<task_id>/<task_status>")
def task_status(task_id, task_status):
    
    task = validate_model(Task,task_id) #record with id = task_id

    # Update task status based on the task_status value
    if task_status == "mark_complete":
        task.completed_at =  datetime.now()

        
        # Send Slack notification
        send_slack_message(f"Someone just completed the task '{task.title}'")

    elif task_status == "mark_incomplete":
        task.completed_at = None # Set to None to indicate incomplete
    else:
        # Return error response for invalid task_status
        return {"error": "Invalid task status provided"}, 400
        
    db.session.commit() #save the changes to db
    return task.to_dict()


@bp.delete("/<task_id>")
def delete_task_by_id(task_id):
    task = validate_model(Task,task_id)
    
    #Delete the task
    db.session.delete(task)
    db.session.commit()
    
    response = {
        "details": f"Task {task.id} \"{task.title}\" successfully deleted"
    }
    return response, 200