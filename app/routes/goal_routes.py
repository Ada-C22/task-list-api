from flask import Blueprint, abort, make_response, request, Response
from ..db import db
from ..models.goal import Goal
from ..models.task import Task
from .route_utilities import validate_model
from datetime import datetime, timezone

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")


@goals_bp.post("")
def create_goal():

    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as e:
        if e.args[0] == "title":
            response = {"details": "Invalid data"}
        return make_response(response, 400)

    db.session.add(new_goal)
    db.session.commit()

    response = {"goal": new_goal.create_response()}

    return response, 201


@goals_bp.post("/<goal_id>/tasks")
def create_tasks_with_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body["task_ids"]
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        task.goal_id = goal.id

        db.session.commit()

    response = {"id": goal.id}
    response.update(request_body)
    return make_response(response)


@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    title_param = request.args.get("title")

    query = query.order_by(Goal.id)
    goals = db.session.scalars(query).all()
    response = [goal.create_response() for goal in goals]

    return response


@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)
    except:
        return make_response({"details": f"Goal {goal_id} not found"}, 404)

    response = {"goal": goal.create_response()}

    return response


@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)
    except:
        return make_response({"details": f"Goal {goal_id} not found"}, 404)

    response_body = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.create_response() for task in goal.tasks],
    }

    return make_response(response_body)


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)
    except:
        return make_response({"details": f"Goal {goal_id} not found"}, 404)

    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    response = {"goal": goal.create_response()}

    return response


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    try:
        goal = validate_model(Goal, goal_id)
    except:
        return make_response({"details": f"Goal {goal_id} not found"}, 404)

    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}

    return response
