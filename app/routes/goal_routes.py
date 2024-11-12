from flask import Blueprint, request, abort, jsonify
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import validate_model
from ..db import db

bp = Blueprint("bp",__name__,url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json() 

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400
    
    title = request_body["title"]
    new_goal = Goal(title=title)

    db.session.add(new_goal)
    db.session.commit()
    
    response = new_goal.to_dict()
    return response, 201

@bp.get("")
def get_all_goals():
    #execute the query statement and retrieve the models
    query = db.select(Goal) #select records from db Model
    
    query = query.order_by(Goal.id)
    goals = db.session.scalars(query) #retrieve the records
    
    response = []
    for goal in goals:
        response.append(goal.to_dict(include_name=False))
    return response 

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    return goal.to_dict()

@bp.put("/<goal_id>")
def update_one_goal_by_id(goal_id):
    goal = validate_model(Goal,goal_id) #record with id = goal_id
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit() 
    return goal.to_dict()

@bp.delete("/<goal_id>")
def delete_goal_by_id(goal_id):
    goal = validate_model(Goal,goal_id)
    
    #Delete the goal
    db.session.delete(goal)
    db.session.commit()
    
    response = {
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
    }
    return response, 200

@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    
    goal = validate_model(Goal, goal_id)    
    request_body = request.get_json()

    task_ids = request_body.get("task_ids")
    if not task_ids:
        response = {"details": "Invalid data"}
        abort(response, 400)
    
    #valid_task_ids = []
    for task_id in task_ids:
        task = validate_model(Task,task_id)
        # assign each task to goal_id
        task.goal_id = goal_id

    response_body = goal.to_dict(include_name=False, tasks_ids=True)
    db.session.commit()

    return response_body , 200

@bp.get("/<goal_id>/tasks")
def get_goals_and_tasks(goal_id):

    goal = validate_model(Goal, goal_id)
    
    # Get associated tasks and convert each to a dictionary
    task_dicts = [task.to_dict(include_name=False , goal_id=True) for task in goal.tasks]
    
    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": task_dicts  # Populate with list of task dictionaries
    }
    
    return response
