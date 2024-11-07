from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.db import db
from sqlalchemy import desc
from app.routes.route_utilities import validate_model_id, delete_record, create_model, get_models_with_filters
from app.models.task import Task


goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@goal_bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)

@goal_bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal)

@goal_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    response = goal.to_dict()

    return {"goal":response}, 200

@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal=validate_model_id(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"title" : goal.title}, 200

@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    return delete_record(Goal, goal_id)

@goal_bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal=validate_model_id(Goal, goal_id)
    request_body=request.get_json()

    task_list= request_body["task_ids"]

    task_objects = [validate_model_id(Task, task_id) for task_id in task_list]
    goal.tasks = task_objects   
    db.session.commit()

    # Alternative:
    # for task in task_list:
    #     task = validate_model_id(Task, task)
    #     task.goal_id = goal.id
    # db.session.commit()

    added_task_ids = [task.id for task in goal.tasks]

    response = {
        "id": goal.id,
        "task_ids": added_task_ids
    }
    return response, 200

@goal_bp.get("/<goal_id>/tasks")
def get_tasks_of_one_goal(goal_id):
    goal = validate_model_id(Goal, goal_id)

    task_list = goal.generate_tasks_list()

    response = goal.to_dict()
    response["tasks"] = task_list
    return response, 200





