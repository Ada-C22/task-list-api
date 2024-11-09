from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from app.routes.routes_utilities import validate_model



goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
    except KeyError as error:
        response_body = {"details":"Invalid data"}
        abort(make_response(response_body, 400))
    
    db.session.add(new_goal)
    db.session.commit()

    response_body = new_goal.to_dict()

    return {"goal": response_body}, 201

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)

    goals = db.session.scalars(query)

    goals_response = [goal.to_dict() for goal in goals]

    return goals_response, 200

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}, 200

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    goal.title = request_body['title']
    db.session.commit()

    return {"goal": goal.to_dict()}, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"}, 200

@goals_bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    task_ids = request_body.get("task_ids")

    if not task_ids:
        return {"msg": "{task_ids} not provided"}, 400

    tasks = Task.query.filter(Task.id.in_(task_ids)).all()

    for task in tasks:
        task.goal_id = goal.id
    
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [task.to_dict() for task in goal.tasks]
    }

    return response, 200
    
    
