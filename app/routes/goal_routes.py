from flask import Blueprint, abort, make_response, Response, request
from .route_utilities import validate_model, create_model, get_models_with_filters
from ..db import db
from app.models.goal import Goal
from app.models.task import Task


goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    return create_model(Goal, request_body)


@goals_bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


@goals_bp.get("/<goal_id>")
def get_one_task(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body.get("title")
    db.session.commit()

    response_body = {"goal": goal.to_dict()}

    return make_response(response_body, 200)


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)  
    db.session.delete(goal)
    db.session.commit()

    response_body = {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }
    return make_response(response_body, 200)


@goals_bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    tasks = request_body.get("task_ids")
    tasks_list = [validate_model(Task, task) for task in tasks]

    goal.tasks = tasks_list
    db.session.commit()

    task_ids = [task.id for task in goal.tasks]

    response = {
        "id": goal.id,
        "task_ids": task_ids
    }

    return response, 200


@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_response = [task.to_dict() for task in goal.tasks]

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_response
    }
  
    return response, 200