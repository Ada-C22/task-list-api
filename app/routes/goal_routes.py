from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal
from app.models.task import Task
from app.routes.task_routes import validate_task_id
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

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
    goal = validate_goal_id(goal_id)

    return {"goal":{
                "id": goal.id,
                "title": goal.title}
            }

def validate_goal_id(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response =  {"message": f"Goal {goal_id} invalid."}
        abort(make_response(response, 400))

    query = db.select(Goal).where(Goal.id==goal_id)
    goal = db.session.scalar(query)
    if not goal:
        response =  {"message": f"Goal {goal_id} not found."}
        abort(make_response(response, 404))   

    return goal    

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    title = request_body.get("title")

    if title is None:

        response = {"details": "Invalid data"}
        return response, 400
    
    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal":{
                "id": new_goal.id,
                "title": new_goal.title}
            }
    return response, 201

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]

    db.session.commit()
    response = {
        "goal":{
                "id": goal.id,
                "title": goal.title} 
            }
    
    return response, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal_id(goal_id)

    db.session.delete(goal)
    db.session.commit()

    response_message = f'Goal {goal.id} "{goal.title}" successfully deleted'
    response_body = {'details': response_message}

    return response_body, 200

@goals_bp.post("/<goal_id>/tasks")
def create_goal_with_tasks(goal_id):
    goal = validate_goal_id(goal_id)
    request_body = request.get_json()
   
    task_list = request_body["task_ids"]
    task_list_in_goal = []
    for task_id in task_list:
    
        task = validate_task_id(task_id)
        task.goal_id = goal.id 
        task_list_in_goal.append(task.id)

    db.session.commit()
    response = {
                "id": goal.id,
                "task_ids": task_list_in_goal}
    
    return response, 200

@goals_bp.get("/<goal_id>/tasks")
def get_goal_with_tasks(goal_id):
    goal = validate_goal_id(goal_id)

    tasks = [task.to_dict() for task in goal.tasks]
    print(f"TEST{tasks}")

    response = {"id": goal.id,
            "title": goal.title,
            "tasks": tasks}
    

    return response

