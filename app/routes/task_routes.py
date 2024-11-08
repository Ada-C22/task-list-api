from flask import Blueprint, abort, make_response, request, Response
from app.models.task import Task
from app.models.goal import Goal
from ..db import db
from sqlalchemy import asc, desc
from datetime import datetime, date
import requests
import os
from dotenv import load_dotenv

load_dotenv()

tasks_bp = Blueprint("tasks_bp", __name__, url_prefix="/tasks")

@tasks_bp.get("")
def get_all_tasks():
    query = db.select(Task)
    sort_order = request.args.get("sort", "asc")
    if sort_order == "desc":
        query = query.order_by(Task.title.desc())
    else:    
        query = query.order_by(Task.title)
    tasks = db.session.scalars(query)
    tasks_response = []
    for task in tasks:
        tasks_response.append(task.to_dict())
        
    return tasks_response, 200

@tasks_bp.get("/<task_id>")
def get_one_task(task_id):
    task = validate_task_id(task_id)
    task_dict = task.to_dict()

    return { "task": task_dict }


def validate_task_id(task_id):
    try:
        task_id = int(task_id)
    except:
        response =  {"message": f"Task {task_id} invalid."}
        abort(make_response(response, 400))

    query = db.select(Task).where(Task.id==task_id)
    task = db.session.scalar(query)
    if not task:
        response =  {"message": f"Task {task_id} not found."}
        abort(make_response(response, 404))   

    return task       

@tasks_bp.post("")
def create_task():
    request_body = request.get_json()

    title = request_body.get("title")
    description = request_body.get("description")
    completed_at = request_body.get("completed_at")

    if title is None or description is None:

        response = {"details": "Invalid data"}
        return response, 400
  
    new_task = Task(title=title, description=description, completed_at=completed_at)
    db.session.add(new_task)
    db.session.commit()

    response = {
        "task":{
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "is_complete": bool(new_task.completed_at)} 
            }
    return response, 201

@tasks_bp.put("/<task_id>")
def update_task(task_id):
    task = validate_task_id(task_id)
    request_body = request.get_json()

    task.title = request_body["title"]
    task.description = request_body["description"]


    db.session.commit()
    response = {
        "task":{
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)} 
            }

    return response, 200

@tasks_bp.delete("/<task_id>")
def delete_task(task_id):
    task = validate_task_id(task_id)

    db.session.delete(task)
    db.session.commit()

    response_message = f'Task {task.id} "{task.title}" successfully deleted'
    response_body = {'details': response_message}

    return response_body, 200

@tasks_bp.patch("/<task_id>/mark_complete")
def mark_task_complete(task_id):
    task = validate_task_id(task_id)
    #now = datetime.now()
    #task.competed_at = now.strftime("%m/%d/%Y")
    task.completed_at = date.today()
    db.session.commit()
 
    url = 'https://slack.com/api/chat.postMessage'
    slack_token = os.environ.get('API_token')
    headers = {'Authorization': f'Bearer {slack_token}'}
    payload = {'channel': 'task-notifications', 'text': f'Someone just completed the task {task.title}'}


    response = requests.post(url, headers=headers, data=payload)

    response = {
            "task":{
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)} 
            }
    return response, 200

@tasks_bp.patch("/<task_id>/mark_incomplete")
def mark_task_incomplete(task_id):
    task = validate_task_id(task_id)
    task.completed_at = None
    db.session.commit()
    response = {
            "task":{
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "is_complete": bool(task.completed_at)} 
            }

    return response, 200