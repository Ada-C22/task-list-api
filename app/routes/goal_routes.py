from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
import datetime
import requests
import os
from sqlalchemy import desc, asc
from .route_utilities import validate_model, create_model

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    return create_model(Goal, request_body)

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    response=[goal.to_dict() for goal in goals]

    return response, 200

@goals_bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response = {"goal": goal.to_dict()}

    return response, 200

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()
    response = {"title": goal.title}

    return response, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    response = {"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}
    
    return response, 200

@goals_bp.post("/<goal_id>/tasks")
def create_task_ids_by_goal(goal_id):
    request_body = request.get_json()
    
    goal = validate_model(Goal, goal_id)

    try:
        task_ids = request_body["task_ids"]

        for task_id in task_ids:
            task = validate_model(Task, task_id)
            goal.tasks.append(task)

        db.session.commit()

    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))

    return {"id": goal.id, "task_ids": task_ids}

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = []

    for task in goal.tasks:
        goal_dict["tasks"].append(task.to_dict())

    return goal_dict