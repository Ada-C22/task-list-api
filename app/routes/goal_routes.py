from flask import Blueprint, request, make_response, abort, jsonify
from app.models.goal import Goal
from app.routes.task_routes import validate_task
from ..db import db

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        response = {"details": "Invalid data"}
        return make_response(response, 400)
    
    title = request_body["title"]

    new_goal= Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201

@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal)
    goals = db.session.scalars(query)

    goals_response = []
    goals_response = [goal.to_dict() for goal in goals]
    return goals_response

@goals_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {
        "goal":goal.to_dict()
        }, 200

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"message": f"goal {goal_id} invalid"}
        abort(make_response(response, 400))

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

    goal.title = request_body.get("title", goal.title)
    db.session.commit()

    return {
        "goal":goal.to_dict()
        }, 200

@goals_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    
    db.session.delete(goal)
    db.session.commit()

    return jsonify({
        "details": f'Goal {goal.id} "{goal.title}" successfully deleted'
    }), 200

@goals_bp.post("/<goal_id>/tasks")
def add_tasks_to_goal(goal_id):
    goal=validate_goal(goal_id)
    request_body=request.get_json()

    task_list= request_body["task_ids"]

    for task in task_list:
        task = validate_task(task)
        task.goal_id = goal_id
    db.session.commit()

    task_ids =[]
    for task in goal.tasks:
        task_ids.append(task.id)

    response = {
        "id": goal.id,
        "task_ids": task_ids
    }
    return response, 200

@goals_bp.get("/<goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = validate_goal(goal_id)
    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks":[task.to_dict() for task in goal.tasks]
    }
    return response




