from flask import Blueprint, request
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal(): 
    request_body = request.get_json()
    return create_model(Goal, request_body)

@goals_bp.get("")
def get_all_goals(): 
    return get_models_with_filters(Goal, request.args)

@goals_bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal":goal.to_dict()}

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    response = {"goal":goal.to_dict()}
    return response

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)    
    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal_id} \"{goal.title}\" successfully deleted'}
    return response

@goals_bp.post("/<goal_id>/tasks")
def assign_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    
    task_ids = request_body["task_ids"]

    for task_id in task_ids:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)

    db.session.commit()

    goal_task_ids = [task.id for task in goal.tasks]

    response = {
        "id": goal.id,
        "task_ids": goal_task_ids
    }
    return response

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    task_list = [task.to_dict() for task in goal.tasks]

    response = goal.to_dict()
    response["tasks"] = task_list
    return response

@goals_bp.delete("/<goal_id>/tasks")
def delete_all_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    for task in goal.tasks:
        db.session.delete(task)
    
    db.session.commit()

    response = {"details": f'All tasks in \"{goal.title}\" are successfully deleted'}
    return response



