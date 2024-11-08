from flask import abort, make_response
from ..db import db
import os
import requests

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as err:
        response = {"details": 'Invalid data'}
        abort(make_response(response , 400))

    db.session.add(new_model)
    db.session.commit()

    return {f'{cls.__name__.lower()}':new_model.to_dict()}, 201

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"details": f"{cls.__name__} {model_id} is invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"details": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

def get_models_by_filters(cls, filters):
    query = db.select(cls)

    

    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    sort_param = filters.get("sort")
    if sort_param == "asc":
        query = query.order_by(cls.title)
    if sort_param == "desc":
        query = query.order_by(cls.title.desc())

    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]

    return models_response

def post_slack_message(task):

    path = "https://slack.com/api/chat.postMessage"

    token = os.environ.get('SLACK_API_KEY')
    headers = {
        "Authorization": f'Bearer {token}'
        }
    post_message = {
        "channel": "api-test-channel",
        "text": f"Someone just completed the task {task.title}"
        }
    
    response = requests.post(path, headers=headers, json=post_message)

    return response
