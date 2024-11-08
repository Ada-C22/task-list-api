from flask import Blueprint, request, make_response, abort
from app.models.goal import Goal
from app.models.task import Task
from ..db import db
from .route_utilities import validate_model

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError as error:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_goal)
    db.session.commit()
    
    return {"goal": new_goal.to_dict()}, 201

@bp.get("")
def get_goals():
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.name.ilike(f"%{title_param}%"))

    goals = db.session.scalars(query.order_by(Goal.id))

    goals_response = [goal.to_dict() for goal in goals]

    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    
    return {"goal": goal.to_dict()}, 200 

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"goal": goal.to_dict()}, 201

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }, 200

@bp.post("/<goal_id>/tasks")
def post_list_of_tasks_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    try:
        task_ids = request_body["task_ids"]
        
        for task_id in task_ids:
            task = validate_model(Task, task_id)
            goal.tasks.append(task)

    except KeyError as error:
        response = {"message": f"Goal {goal_id} not found"}
        abort(make_response(response, 404))
        
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }, 200

@bp.get("/<goal_id>/tasks")
def get_task_of_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    tasks = goal.tasks

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": [
            {
                "id": task.id,
                "goal_id": goal.id,
                "title": task.title,
                "description": task.description, 
                "is_complete": bool(task.completed_at)
            }
            for task in tasks
        ]
    }, 200