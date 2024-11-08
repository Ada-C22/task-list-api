from flask import Blueprint, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from app.routes.route_utilities import validate_model

from app.db import db

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        response_body = {"details": "Invalid data"}
        return make_response(response_body, 400)
    
    title = request_body["title"]
    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()
    
    response_body = {"goal": new_goal.goal_dict()}
    return response_body, 201

@bp.get("")
def get_all_saved_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)
    
    response_body = [goal.goal_dict() for goal in goals]
    return response_body

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.add(goal)
    db.session.commit()

    response_body = {"goal": goal.goal_dict()}
    return response_body

@bp.put("/<goal_id>")
def update_one_goal(goal_id):
    goal= validate_model(Goal, goal_id)
    
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    
    response_body = {"goal": goal.goal_dict()}
    return make_response(response_body, 200)

@bp.delete("/<goal_id>")
def delete_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    db.session.delete(goal)
    db.session.commit()
    
    response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return make_response(response, 200)

@bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])
    
    body_task_ids = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)
        if task:
            task.goal_id = goal_id
            body_task_ids.append(task_id)    
    
    db.session.commit()
    
    tasks_of_goal = [task.id for task in goal.tasks]
    response_body = {
        "id": goal.id,
        "task_ids": tasks_of_goal # return all tasks including previous tasks
    }
    return response_body

@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    response_body = dict(
        id=goal.id,
        title=goal.title,
        tasks=[task.task_dict() for task in goal.tasks]
    )
    return response_body
    
    
