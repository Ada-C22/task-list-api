from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from datetime import datetime
from ..db import db
from .task_routes import validate_task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    title = request_body["title"]
    

    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    
    response = { "goal" : {
        "id": new_goal.id,
        "title": new_goal.title
    }
    }
    return response, 201

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )
    return goals_response, 200

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return { "goal" : {
                "id": goal.id,
                "title": goal.title
            }
    }

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"goal {goal_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"goal {goal_id} not found"}
        abort(make_response(response, 404))
    return goal


@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()


    response = { "goal" : {
                "id": goal.id,
                "title": goal.title
            }
    }
    return response, 200


@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f"Goal {goal.id} \"{goal.title}\" successfully deleted"
    }
    
    return response, 200



@goals_bp.post("/<goal_id>/tasks")
def create_task_with_goal(goal_id):
    goal = validate_goal(goal_id)

    request_data = request.get_json()
    task_ids = request_data.get("task_ids")

    if not task_ids:
        response = {"message": "No task_ids provided"}
        abort(make_response(response, 400))

    for task_id in task_ids:
        task = validate_task(task_id)
        task.goal = goal  

    db.session.commit()

    response_body = {
        "id": goal.id,
        "task_ids": task_ids
    }
    return response_body, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    goal = validate_goal(goal_id)
    
    tasks = [{
        "id": task.id,
        "goal_id": goal.id,
        "title": task.title,
        "description": task.description,
        "is_complete": task.completed_at is not None
    } for task in goal.tasks]
    
    response_body = {"id": goal.id,
        "title": goal.title,
        "tasks": tasks}
    
    return response_body, 200

