from flask import abort, make_response, request
from ..db import db
import os
import requests

# Slack webhook URL and token from environment variables
SLACK_URL = "https://slack.com/api/chat.postMessage"
SLACK_TOKEN = os.environ.get("SLACK_BOT_TOKEN")

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except ValueError:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    #execute the query statement and retrieve the models
    query = db.select(cls).where(cls.id == model_id) #select records with an id = model_id
    model = db.session.scalar(query) #retrieve only one record model_id

    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))

    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]
    return models_response

def send_slack_message(message):
    # Sends a message to the Slack channel using the Slack API.

    headers = {
        "Authorization": f"Bearer {SLACK_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": "tasks-api-notifications",
        "text": message
    }
    response = requests.post(SLACK_URL, headers=headers, json=payload)
    response.raise_for_status()  # Raise an error if the request fails


