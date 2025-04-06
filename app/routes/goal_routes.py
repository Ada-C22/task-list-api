from flask import Blueprint, abort, jsonify, make_response, request
from app.db import db
from ..models.goal import Goal
import requests
# from .route_utilities import validate_model, create_model, validate_task, validate_goal
from app.models.task import Task
from ..routes.task_routes import validate_task


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():

    try:
        request_body = request.get_json()
        title = request_body["title"]
        
        new_goal = Goal(title=title)

        db.session.add(new_goal)
        db.session.commit()

        return {"goal": new_goal.to_dict()}, 201
    
    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

@bp.get("")
def get_all_goals():

    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = [goal.to_dict() for goal in goals]

    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    response = {"goal": goal.to_dict()}
    return response


@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_goal(goal_id)
    response = goal.to_nested_dict()
    return response

# @bp.get("/<goal_id>/tasks")
# def get_tasks_for_one_goal(goal_id):
#     goal = validate_goal(goal_id)
#     return goal.to_nested_dict()



@bp.post("/<goal_id>/tasks")
def create_new_tasks_for_goal(goal_id):
    
    current_goal = validate_goal(goal_id)
    request_body = request.get_json()
    
        
    current_goal_tasks = request_body["task_ids"]

    for task in current_goal_tasks:
        current_task = validate_task(task)
        # query = db.select(Task).where(current_task.goal_id == goal_id)
        current_task.goal_id = goal_id

    db.session.commit()

    return {"id": current_goal.id,
            "task_ids": current_goal_tasks
        }


@bp.delete("/<goal_id>")
def delete_goal(goal_id):

    goal = validate_goal(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return jsonify(response)

    
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    return {"goal": goal.to_dict()}


def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    
    except:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"details": f"Goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal