from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model, create_model
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    return {"goal": create_model(Goal, request_body)}, 201
    

@goals_bp.get("")
def get_all_tasks():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )
    return goals_response

@goals_bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal.id} "{goal.title}" successfully deleted'}
    return response, 200


@goals_bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    task_ids = request_body["task_ids"]
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids": task_ids}
    return response, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }
    return response, 200
