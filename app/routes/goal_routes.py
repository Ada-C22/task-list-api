from flask import Blueprint, abort, make_response, request, Response
from app.models.goal import Goal  
from ..db import db
from datetime import datetime, timezone

goals_bp = Blueprint("goals_bp", __name__, url_prefix="/goals")

##refactor validate!! 
@goals_bp.post("/<goal_id>/tasks")
def create_goal_with_task(goal_id):
    goal = validate_model(Goal, goal_id)

    request_body = request.get_json()
    request_body["goal_id"] = goal.id

    try:
        new_task = Task.from_dict(request_body)
    except KeyError as error:
        response = {"message": f"Invalid requests: missing {error.ergs[0]}"}
        abort(make_response(response, 400))
    db.session.add(new_task)
    db.session.commit()

    return make_response(new_task.to_dict(), 201)

@goals_bp.post("")
def create_goal():
    request_body = request.get_json()

    # Validate request data
    if "title" not in request_body:
        response = {"details": "Invalid data"}
        return make_response(response, 400)

    title = request_body["title"]

    # Create new goal instance
    new_goal = Goal(title=title)
    
    # Add new goal to the database session and commit
    db.session.add(new_goal)
    db.session.commit()

    response = {
        "goal": { 
            "id": new_goal.id,
            "title": new_goal.title,
        }
    }

    return response, 201

@goals_bp.get('/<goal_id>')
def get_one_goal(goal_id):
    goal = validate_goal(goal_id)

    return {
        "goal":{
        "id": goal.id,
        "title": goal.title,
        }
    }


@goals_bp.get("")
def get_all_goals():
    query = db.select(Goal).order_by(Goal.id)
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

@goals_bp.put("/<goal_id>")
def update_goal(goal_id):
    goal = validate_goal(goal_id)
    request_body = request.get_json()

    goal.title = request_body["title"]
    
    db.session.commit()

    return {
        "goal": {
            "id": goal.id,
            "title": goal.title,       
        }
    }, 200
    
@goals_bp.delete("<goal_id>")
def delete_task(goal_id):
    goal = validate_goal(goal_id)
    db.session.delete(goal)
    db.session.commit()

    return {"details":f'Goal {goal_id} "{goal.title}" successfully deleted'},200 
    # Response(status=204, mimetype="application/json")

def validate_goal(goal_id):
    try:
        goal_id = int(goal_id)
    except ValueError:
        response = {"message": f"goal {goal_id} invalid"}
        abort(make_response(response,400))

    query = db.select(Goal).where(Goal.id == goal_id)
    goal = db.session.scalar(query)

    if not goal:
        response = {"message": f"goal {goal_id} not found"}
        abort(make_response(response, 404))

    return goal