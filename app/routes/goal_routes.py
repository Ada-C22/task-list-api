from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model, get_model_with_filters, create_model



bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        abort(make_response({"details": "Invalid data"}, 400))
        
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": new_goal.to_dict()  
    }
    return response, 201

@bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    from app.models.goal import Goal
    from app.models.task import Task

    goal = validate_model(Goal, goal_id)
    if not goal:
        response = {"message": f"Goal with ID {goal_id} not found"}
        abort(make_response(response, 404))

    request_body = request.get_json()
    task_ids = request_body.get("task_ids")
    
    if not task_ids:
        response = {"message": "Invalid request: missing 'task_ids'"}
        abort(make_response(response, 400))

    tasks = Task.query.filter(Task.id.in_(task_ids)).all()

    if len(tasks) != len(task_ids):
        response = {"message": "One or more tasks not found"}
        abort(make_response(response, 404))

    for task in tasks:
        if task not in goal.tasks:
            goal.tasks.append(task)

    db.session.commit()

    goal_data = {
        "id": goal.id,
        "task_ids": [task.id for task in goal.tasks]
    }

    response = goal_data  
    return response, 200


@bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    from app.models.goal import Goal
    from app.models.task import Task
    goal = validate_model(Goal, goal_id)


    if goal.tasks:  
        task_data = [task.to_dict() for task in goal.tasks]
    else: 
        tasks = Task.query.filter_by(goal_id=goal.id).all()
        task_data = [
            task.to_dict() for task in tasks
        ]

    task_data = task_data or []

    for task in task_data:
        task["is_complete"] = bool(task.get("is_complete", False))  # Explicitly cast to bool

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": task_data 
    }

    return response, 200

@bp.get("/tasks/<task_id>")
def get_task_by_id(task_id):
    from app.models.task import Task
    from app.models.goal import Goal
    
    # Validate that the task exists
    task = Task.query.get(task_id)
    if not task:
        response = {"message": f"task id {task_id} not found"}
        abort(make_response(response, 404))
    
    task_data = {
        "id": task.id,
        "goal_id": task.goal_id,  
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None 
    }
    
    return {"task": task_data}, 200



@bp.get("")
def get_all_goal():
    return get_model_with_filters(Goal, request.args)

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if not goal:
        abort(make_response({"message": f"goal_id {goal_id} not found"}, 404))
    goal_response = {
        "goal": goal.to_dict()  
    }

    return goal_response, 200


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if not goal:
        abort(make_response({"message": f"goal_id {goal_id} not found"}, 404))
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()

    response = {
        "goal": goal.to_dict()  
    }

    return response, 200

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    if not goal:
        abort(make_response({"message": f"goal_id {goal_id} not found"}, 404))
    
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }

    return response, 200
