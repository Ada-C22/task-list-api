from flask import Blueprint, request
from app.models.goal import Goal
from app.models.task import Task
from app.db import db

goals_bp = Blueprint("goals", __name__, url_prefix="/goals")

@goals_bp.post("")
def create_goal():
    request_data = request.get_json()
    title = request_data.get("title")
     
    if not title:
        return {"details": "Invalid data"}, 400
     
    goal = Goal(title=title)
    db.session.add(goal)
    db.session.commit()

    return {"goal": {"id": goal.id, "title": goal.title}}, 201

# Get All Goals
@goals_bp.get("")
def get_goals():
    goals = Goal.query.all()
    return [
        {
            "id": goal.id,
            "title": goal.title
        }
        for goal in goals
    ], 200

# Get One Goal by ID
@goals_bp.get("/<int:goal_id>")
def get_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if goal:
        return {
            "goal": {
                "id": goal.id,
                "title": goal.title
            }
        }, 200
    return {
        "message": f"Goal {goal_id} not found"
    }, 404

@goals_bp.put("/<int:goal_id>")
def update_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {"message": f"Goal {goal_id} not found"}, 404

    request_data = request.get_json()
    title = request_data.get("title")

    if not title:
        return {"details": "Invalid data"}, 400

    goal.title = title
    db.session.commit()

    return {
        "goal": {
            "id": goal.id,
            "title": goal.title
        }
    }, 200

@goals_bp.delete("/<int:goal_id>")
def delete_goal(goal_id):
    goal = Goal.query.get(goal_id)
    
    if not goal:
        return {
            "message": f"Goal {goal_id} not found"
        }, 404

    db.session.delete(goal)
    db.session.commit()

    return {
        "details": f'Goal {goal_id} "{goal.title}" successfully deleted'
    }, 200


@goals_bp.post("/<int:goal_id>/tasks")
def post_task_ids_to_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {
            "message": f"Goal {goal_id} not found"
        }, 404

    request_data = request.get_json()
    task_ids = request_data.get("task_ids", [])

    tasks = Task.query.filter(Task.id.in_(task_ids)).all()

    if len(tasks) != len(task_ids):
        return {
            "message": "Some task IDs are invalid"
        }, 400

    for task in tasks:
        task.goal_id = goal.id 
    db.session.commit()

    return {
        "id": goal.id,
        "task_ids": [task.id for task in tasks]  
    }, 200

@goals_bp.get("/<int:goal_id>/tasks")
def get_tasks_for_goal(goal_id):
    goal = Goal.query.get(goal_id)
    if not goal:
        return {
            "message": f"Goal {goal_id} not found"
        }, 404

    tasks = goal.tasks

    return {
        "id": goal.id,
        "title": goal.title,
        "tasks": [
            {
                "id": task.id,
                "goal_id": task.goal_id,
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            } for task in tasks
        ]
    }, 200
