from flask import Blueprint, request, abort, make_response
from app.models.goal import Goal
from app.models.task import Task
from app.db import db
from app.routes.route_utilities import validate_model

bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

@bp.post("")
def create_goal():
    request_body = request.get_json()

    if "title" not in request_body:
        return {"details": "Invalid data"}, 400

    title = request_body["title"]

    new_goal = Goal(title=title)
    db.session.add(new_goal)
    db.session.commit()

    return {"goal": new_goal.to_dict()}, 201
    

@bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
    goals = db.session.scalars(query)

    return [goal.to_dict() for goal in goals]
    

@bp.get("/<goal_id>")
def get_single_goal(goal_id):

    goal = validate_model(Goal, goal_id)
    return {"goal": goal.to_dict()}


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    db.session.commit()

    return {"goal": goal.to_dict()}


@bp.delete("/<goal_id>")
def delete_task(goal_id):
    goal = validate_model(Goal, goal_id)

    db.session.delete(goal)
    db.session.commit()

    return {"details": f'Goal {goal_id} "Build a habit of going outside daily" successfully deleted'}


@bp.post("/<goal_id>/tasks")
def post_tasks_ids_to_goal(goal_id):
    goal = validate_model(Goal, goal_id)
    request_body = request.get_json()
    task_ids = request_body.get("task_ids", [])

    if not task_ids:
        response = {"message": "Invalid request: missing task_ids"}
        abort(make_response(response, 400))

    tasks_to_add = []
    for task_id in task_ids:
        task = validate_model(Task, task_id)

        if task not in goal.tasks:
            tasks_to_add.append(task)

    if tasks_to_add:
        goal.tasks.extend(tasks_to_add)
        try:
            db.session.add(goal)
            db.session.commit()
        except Exception as e:
            response = {
                "message": f"Failed to update goal with tasks: {str(e)}"}
            abort(make_response(response, 500))

    return {"id": goal.id, "task_ids": task_ids}, 200


@bp.get("/<goal_id>/tasks")
def get_tasks_for_specific_goal(goal_id):
    goal = validate_model(Goal, goal_id)

    response = {
        "id": goal.id,
        "title": goal.title,
        "tasks": [
            {
                "id": task.id,
                "goal_id": goal.id,  
                "title": task.title,
                "description": task.description,
                "is_complete": task.completed_at is not None
            }
            for task in goal.tasks
        ]
    }

    return response, 200
