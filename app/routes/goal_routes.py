from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from app.routes.route_utilities import validate_model
from ..db import db
from app.models.task import Task
goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():

    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    new_goal = Goal(title=request_body["title"])
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": {
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
                "title": goal.title,
            }
        )

    return goals_response

@goals_bp.get("/<goals_id>")
def get_one_goal(goals_id):
    goal = validate_model(Goal, goals_id)
    query = db.select(Goal).where(Goal.id == goals_id)
    goal = db.session.scalar(query)
    return {
                "goal": {
                    "id": goal.id,
                    "title": goal.title,
                }
            }

@goals_bp.put("/<goals_id>")
def update_goal(goals_id):
    goal = validate_model(Goal, goals_id)
    request_body = request.get_json()

    goal.title = request_body['title']

    db.session.commit()

    return {
                "goal": {
                    "id": goal.id,
                    "title": goal.title,
                }
            }

@goals_bp.delete("/<goals_id>")
def delete_goal(goals_id):
    goal = validate_model(Goal, goals_id)
    db.session.delete(goal)
    db.session.commit()

    return {"details": f"Goal {goals_id} \"{goal.title}\" successfully deleted"}

@goals_bp.post("/<goals_id>/tasks")
def create_task_list_for_goal(goals_id):

    goal = validate_model(Goal, goals_id)

    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    tasks = Task.query.filter(Task.id.in_(task_ids)).all()

    goal.tasks = tasks
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }

@goals_bp.get("/<goals_id>/tasks")
def get_tasks_by_goal(goals_id):
    goal = validate_model(Goal, goals_id)
    tasks = [task.to_dict() for task in goal.tasks]
    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }


    

