from flask import Blueprint,request,abort,make_response
from app.models.goal import Goal
from ..db import db
from .route_utilities import validate_model
from app.models.task import Task


bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)
     
    except KeyError as error:
        response = {"details":f"Invalid data"}
        abort(make_response(response,400))
    
    db.session.add(new_goal)
    db.session.commit()

    response = {"goal" : new_goal.to_dict()}
    return response,201
    
@bp.get("")
def get_all_goals():
    
    query = db.select(Goal)
    sorted_title = request.args.get("sort")
    if sorted_title == "desc":
        query = query.order_by(Goal.title.desc())
    else:
        query = query.order_by(Goal.title.asc())
                            
    goals = db.session.scalars(query)

    goals_response =([goal.to_dict() for goal in goals],200)
    
    return goals_response

@bp.get("/<goal_id>")
def get_single_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    return {"goal" : goal.to_dict()}

@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()


    goal.title = request_body["title"]
   
    db.session.commit()
    return {"goal" : goal.to_dict()}

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": 'Goal 1 "Build a habit of going outside daily" successfully deleted'
    }

@bp.post("/<goal_id>/tasks")
def create_task_with_goal_id(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()

    task_ids = request_body["task_ids"] 
    for task_id in task_ids:    
        new_task_id = validate_model(Task, task_id)

        goal.tasks.append(new_task_id)

    db.session.commit()

    response = {
        "id": goal.id,
        "task_ids" : task_ids
    }

    return  response

@bp.get("/<goal_id>/tasks")
def get_tasks_of_goal(goal_id):
    goal = validate_model(Goal,goal_id)

    all_tasks= []
    for task in goal.tasks:
        all_tasks.append(task.to_dict())

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": all_tasks
        }
         
    return response 
