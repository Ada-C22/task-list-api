from flask import abort, make_response
from app.db import db
from app.models.goal import Goal
from app.models.task import Task
import requests
import os

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} {model_id} is invalid, should be an int data type"}, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} is not found"}, 404))
    
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        abort(make_response({'details': 'Invalid data'}, 400))
    
    db.session.add(new_model)
    db.session.commit()

    response = new_model.to_dict_without_goal_id() if hasattr(new_model, "goal") else new_model.to_dict()
    return make_response(response, 201)
    
def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    if filters:
        sort_param = filters.get("sort") 
        if sort_param == "desc":
            query = query.order_by(getattr(cls, "title").desc())
        else:
            query = query.order_by(getattr(cls, "title").asc())

        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict_without_goal_id()["task"] for model in models]

    return models_response

def notify_slack(task):
    url = "https://slack.com/api/chat.postMessage"
    token = os.environ.get('SLACKBOT_TOKEN')
    header = {"Authorization": f"Bearer {token}"}
    request_body = {
        "channel": "C07TDEQ17RQ",
        "text": f"Someone just completed the task {task.title}"
    }

    return requests.post(url, json=request_body, headers=header)
