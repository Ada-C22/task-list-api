from flask import Blueprint, make_response, abort, request

from app import db
from app.models.goal import Goal
from app.models.task import Task

goal_bp = Blueprint("goal_bp", __name__, url_prefix="/goals")

def validate_key_in_request(request_body, key, datatype):
    if key not in request_body or not isinstance(request_body[key], datatype):
        abort(make_response({"details": "Invalid data"}, 400))
    return request_body


def validate_goal_id(id):
    if not id.isnumeric():
        abort(make_response({"details": f" {id} Invalid data"}, 400))


@goal_bp.post("")
def create_goal():
    request_body = validate_key_in_request(request.get_json(), "title", str)
    new_goal = Goal().from_dict(request_body)
    db.session.add(new_goal)
    db.session.commit()
    response = {
        "goal": new_goal.to_dict()
    }
    return response, 201


@goal_bp.get("")
def get_all_tasks():
    title_param = request.args.get("title")

    query = db.select(Goal)
    if title_param:
        query = query.where(Goal.title.like(f"%{title_param}"))

    goals = db.session.scalars(query).all()
    return [goal.to_dict() for goal in goals]




@goal_bp.get("/<goal_id>")
def get_one_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    return {"goal": goal.to_dict()}


@goal_bp.post("/<goal_id>/tasks")
def set_one_goal_tasks(goal_id):
    request_body = validate_key_in_request(request.get_json(), "task_ids", list)
    goal = get_goal_by_id(goal_id)
    task_ids = request_body.get("task_ids", [])

    tasks = db.session.query(Task).filter(Task.id.in_(task_ids)).all()
    if len(tasks) != len(task_ids):
        abort(make_response({"message": "One or more tasks not found"}, 404))

    for task in tasks:
        task.goal = goal

    db.session.commit()

    return {"id": goal.id, "task_ids": [task.id for task in tasks]}, 200


@goal_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    request_body = request.get_json()
    goal.title = request_body["title"]
    db.session.commit()
    result = {"goal": goal.to_dict()}
    return make_response(result, 200)


@goal_bp.delete("/<goal_id>")
def delete_goal(goal_id):
    goal = get_goal_by_id(goal_id)
    db.session.delete(goal)
    db.session.commit()
    response = {"details": f'Goal {goal_id} "{goal.title}" successfully deleted'}
    return make_response(response, 200)


def get_goal_by_id(goal_id):
    validate_goal_id(goal_id)
    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"Goal {goal_id} not found"}
        abort(make_response(response, 404))
    return goal


@goal_bp.get("/<goal_id>/tasks")
def get_one_goal_tasks(goal_id):
    return get_goal_by_id(goal_id).to_dict(False)
     
