from flask import Blueprint, request, Response, make_response, abort
from app.models.goal import Goal
from ..db import db
from ..models.task import Task
from ..routes.task_routes import validate_task

bp = Blueprint("goals_bp", __name__, url_prefix="/goals" )

@bp.post("")
def create_goal():
    request_body = request.get_json()

    try:
        new_goal = Goal.from_dict(request_body)

    except KeyError as e:
        response = {
            "details": "Invalid data"
        }
        abort(make_response(response, 400))

    db.session.add(new_goal)
    db.session.commit()

    return new_goal.to_dict(), 201

@bp.get("")
def get_all_goals():
    query = db.select(Goal)

    title_param = request.args.get("title")
    if title_param:
        query = query.where(Goal.title.ilike(f"%{title_param}%"))

    sort_param = request.args.get("sort")
    if sort_param:
        if sort_param == "asc":
            query = query.order_by(Goal.title.asc())
        elif sort_param == "desc":
            query = query.order_by(Goal.title.desc())

    query = query.order_by(Goal.id)
    goals = db.session.scalars(query)

    goals_response = []
    for goal in goals:
        goals_response.append(
            {
                "id": goal.id,
                "title": goal.title
            }
        )

    return goals_response

@bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return goal.to_dict()


@bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    response = {
    "goal": {
        "id": goal.id,
        "title": goal.title
        }   
    }

    return response, 200

@bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    response = {
        "details": f"Goal {goal_id} \"{goal.title}\" successfully deleted"
    }

    return response, 200

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except:
        response = {"details": "Invalid data"}

        abort(make_response(response , 400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)
    
    if not goal:
        response = {"message": f"Goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal

@bp.post("/<goal_id>/tasks")
def assign_tasks_to_goal(goal_id):
    goal = validate_goal(goal_id)
    
    request_body = request.get_json()
    task_ids = request_body["task_ids"]

    for task_id in task_ids:
        task = validate_task(task_id)
        task.goal_id = goal_id
        db.session.add(task)

    db.session.commit()

    response = {
        "id": int(goal_id),
        "task_ids": task_ids
    }

    return response, 200

@bp.get("/<goal_id>/tasks")
def get_goal_with_assigned_tasks(goal_id):
    goal = validate_goal(goal_id)

    query = db.select(Task).where(Goal.id == goal_id)

    tasks = db.session.scalars(query)

    response = {}
    response["id"] = goal.id
    response["title"] = goal.title
    response["tasks"] = []

    response["tasks"] = [task.to_dict() for task in tasks]

    return response, 200
