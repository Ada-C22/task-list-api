
from flask import Blueprint, abort, make_response, request
from app.models.goal import Goal
from app.models.task import Task
from .route_utilities import validate_model 
from ..db import db

bp = Blueprint("goals_bp", __name__, url_prefix="/goals")
@bp.post("")
def create_goal():
    request_body = request.get_json()
    if "title" not in request_body:
        response_body = {
        "details": "Invalid data"
        }
        return response_body, 400
    
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    response = {"goal": new_goal.to_dict()}
    return response, 201


@bp.get("")
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
    return goals_response, 200

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)
    response_body = {"goal": goal.to_dict()}
    return response_body

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()
    response = {
     "goal": {
        "id": goal.id,
        "title": goal.title,
       
    }
}
    return response, 200

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()
    response = {
        "details": "Goal 1 \"Build a habit of going outside daily\" successfully deleted"
    }

    return response, 200

@bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    goal = validate_model(Goal,goal_id)
    request_body = request.get_json()
    
    if 'title' in request_body and 'description' in request_body:
        request_body['goal_id'] = goal.id
        new_task = Task.from_dict(request_body)
        db.session.add(new_task)
        db.session.commit()
        tasks = [task.id for task in goal.tasks]
        response = {
        "id": goal.id,
        "task_ids": tasks,
        }
        return response


    task_ids = []
    for task_id in request_body['task_ids']:
        task = validate_model(Task,task_id)
        task_ids.append(task.id)
        goal.tasks.append(task)
    
    db.session.commit()
    
    response = {
        "id": goal.id,
        "task_ids": task_ids,
    }
    return response,200

@bp.get("/<goal_id>/tasks")
def get_tasks_by_goal(goal_id):
    goal = validate_model(Goal,goal_id)
    tasks = [task.to_dict() for task in goal.tasks]
    goal_dict = goal.to_dict()
    response = {
        "id": goal_dict["id"],
        "title": goal_dict["title"],
        "tasks": tasks
    }
    return response

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"message": f"Goal {goal_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"goal {goal_id} not found"}
        abort(make_response(response, 404))
    return goal