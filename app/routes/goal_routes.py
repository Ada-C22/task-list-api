from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
import os
import requests
from ..db import db
from .route_utilities import validate_model, create_model, get_models_with_filters

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


# CREATE
@bp.post("")
def create_goal():
    request_body = request.get_json()
    response = create_model(Goal, request_body)
    goal_dict = response.get_json()
    return make_response({"goal": goal_dict}, 201)


# GET ALL
@bp.get("")
def get_all_goals():
    return get_models_with_filters(Goal, request.args)


# GET ONE
@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.to_dict()}, 200


# UPDATE
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"goal": goal.to_dict()}, 200

# DELETE
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_title = goal.title
    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "{goal_title}" successfully deleted'}, 200


@bp.post("/<goal_id>/tasks")
def handle_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    if "task_ids" in request_body:
        # Handle associating existing tasks
        task_ids = request_body["task_ids"]
        for task_id in task_ids:
            task = validate_model(Task, task_id)
            if task not in goal.tasks:
                goal.tasks.append(task)

        db.session.commit()

        return {"id": goal.id, "task_ids": [task.id for task in goal.tasks]}, 200
    else:
        # Handle creating new task
        request_body["goal_id"] = goal.id
        return create_model(Task, request_body)


@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": [
            task.to_dict()
            for task in goal.tasks
        ],
    }
