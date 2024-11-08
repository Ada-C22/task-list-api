from flask import Blueprint, request
from .route_utilities import create_model, validate_model
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import create_model, validate_model, get_models_by_filters
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@bp.get("")
def get_all_goals():
    return get_models_by_filters(Goal, request.args)

@bp.get("<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}

@bp.put("<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {'goal': goal.to_dict()}

@bp.delete("<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'{Goal.__name__} {goal.id} "{goal.title}" successfully deleted'
        }

@bp.post("<goal_id>/tasks")
def add_task_with_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = []
    for task_id in request_body["task_ids"]:
        task = validate_model(Task, task_id)
        task_ids.append(task.id)
        goal.tasks.append(task)

    db.session.commit()

    return dict(
        id=int(goal_id),
        task_ids=task_ids
    )

@bp.get("<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    goal_dict = goal.to_dict()
    goal_dict["tasks"] = [task.to_dict() for task in goal.tasks]

    return goal_dict

@bp.get("<goal_id>/tasks/<task_id>")
def get_one_task_by_goal(goal_id, task_id):

    goal = validate_model(Goal, goal_id)
    task = validate_model(Task, task_id)
    
    if task in goal.tasks:
        goal_dict = goal.to_dict()
        goal_dict["task"] = task.to_dict() 
        return goal_dict
    return {"details": f"Task {task.id} not found for Goal {goal.id}"}, 404
