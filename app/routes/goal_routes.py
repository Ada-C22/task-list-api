from flask import Blueprint
from app import db
from app.models.goal import Goal
from flask import request
from app.models.task import Task

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()
    
    if "title" not in request_body:
        return {
            "details": "Invalid data"
        }, 400 
        
    new_goal = Goal.from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    
    return {
        "goal": new_goal.to_dict()
    }, 201
    

@goals_bp.get("")
def get_goals():
    goals = Goal.query.all()
    goals_list = [goal.to_dict() for goal in goals]
    return goals_list, 200

@goals_bp.get("/<goal_id>")
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if not goal:
        return {"message": f"goal {goal_id} not found"}, 404
    return {
        "goal": goal.to_dict()
        }, 200

@goals_bp.get("/<goal_id>/tasks")
def get_goal_tasks(goal_id):
    # Get the goal
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"goal {goal_id} not found"}, 404
    
    tasks = [task.to_dict_with_goal() for task in goal.tasks] 

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": tasks
    }, 200
    
@goals_bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    # Get the goal
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"goal {goal_id} not found"}, 404

    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    # Get all tasks with the provided IDs
    tasks = Task.query.filter(Task.id.in_(task_ids)).all()
    
    for task in tasks:
        task.goal_id = goal.id

    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": task_ids
    }, 200
    
@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"goal { goal_id} not found"}, 404
    
    request_body = request.get_json()
    goal.title = request_body["title"]
    
    db.session.commit()
    
    return {
        "goal": goal.to_dict()
    }, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"goal {goal_id} not found"}, 404
    
    goal_id = goal.id
    goal_title = goal.title
    
    # Delete the goal
    db.session.delete(goal)
    db.session.commit()
    
    return {
        "details": f'Goal {goal_id} "{goal_title}" successfully deleted'
    }, 200
    


