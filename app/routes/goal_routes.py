from flask import Blueprint, Response, request, abort, make_response
from ..models.goal import Goal
from ..db import db
from ..models.task import Task
from .route_utilities import validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    new_goal = Goal.obj_from_dict(request_body)

    db.session.add(new_goal)
    db.session.commit()
    response = {"goal": new_goal.obj_to_dict()}
    return response, 201

@bp.post("/<goal_id>/tasks")
def add_tasks_to_goals(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body["task_ids"]
    tasks = Task.query.filter(Task.id.in_(task_ids)).all()
    goal.tasks = tasks

    db.session.commit()
    response = {
        "id": goal.id,
        "task_ids": task_ids
    }

    return response, 200


@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = [goal.obj_to_dict() for goal in goals]
    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal": goal.obj_to_dict()}, 200

# get all tasks of a certain goal
@bp.get("/<goal_id>/tasks")
def get_all_tasks_of_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks_list = [task.obj_to_dict() for task in goal.tasks]
    print(tasks_list)
    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks_list
    }

    return response, 200


@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    goal.title = request_body["title"]

    db.session.commit()

    response = {"goal": goal.obj_to_dict()}
    return response, 200


@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()
    
    response = {"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}
    return response, 200


