from flask import Blueprint, abort, make_response, request, Response

from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from datetime import datetime
from app.routes.utilities_routes import *

bp = Blueprint("goal_bp",__name__, url_prefix= "/goals")


####################################################################
######################### Create FUNCTIONS #########################
####################################################################
@bp.post("")
def create_goal():
    request_body = request.get_json()
    
    if not request_body or not request_body.get("title"):
        return make_response({"details": "Invalid data: missing title"}, 400) 
    
    goal = create_model(Goal, request_body)
    return make_response(goal, 201)


@bp.post("/<goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    request_body = request.get_json() 
    goal = validate_model(Goal, goal_id)

    task_ids = request_body.get("task_ids", [])
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        goal.tasks.append(task)
    
    db.session.commit()

    response_body = { 
        "id": goal.id, 
        "task_ids": [task.id for task in goal.tasks]
    }


    return response_body, 200


####################################################################
######################### READ FUNCTIONS #########################
####################################################################

@bp.get("")
def get_goals():
    request_arguements = request.args
    goals = get_models_with_filters(Goal, request_arguements)
    if not goals: 
        return make_response([], 200)
    
    return make_response(goals, 200)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    try: 
        goal = validate_model(Goal, goal_id)
        return make_response({"goal": goal.to_dict()}, 200)
    except: 
        return make_response({"details": f"Goal {goal_id} not found"}, 404)

@bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    response_body = goal.to_dict()
    response_body["tasks"] = [task.to_dict() for task in goal.tasks]
    return response_body, 200
    
####################################################################
######################### UPDATE FUNCTIONS #########################
####################################################################
@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal_title = request_body.get("title")
    if not goal_title: 
        return make_response({"details": "Invalid request: missing title"}, 400)
    goal.title = goal_title 
    db.session.commit()

    return make_response({"goal": goal.to_dict()}, 200)


####################################################################
######################### DELETE FUNCTIONS #########################
####################################################################
@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    goal_id = goal.id
    goal_title = goal.title 

    db.session.delete(goal)
    db.session.commit()

    response_body = { 
        "details": f'Goal {goal_id} "{goal_title}" successfully deleted'
    }
    return make_response(response_body, 200)
