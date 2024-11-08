from flask import abort, make_response
from ..db import db
import os
import requests

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"message": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response , 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        response = {"message": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))
    
    return model

def send_slack_message(task_title):
    path = "https://slack.com/api/chat.postMessage"
    headers = {"Authorization" :os.environ.get('SLACK_API_TOKEN')}
    data = {
    "channel": "C080EU3HERW",
    "text" : f"Someone just completed the task: {task_title}"
    }
    
    requests.post(path,data=data,headers=headers)