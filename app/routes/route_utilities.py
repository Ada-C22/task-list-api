from flask import abort, make_response
from ..db import db
from app.models.task import Task
from app.models.goal import Goal
from sqlalchemy import desc, asc

def validate_model(cls, model_id):

    # checks for valid input
    try: 
        model_id = int(model_id)
    except: 
        abort(make_response({"msg": f"{cls.__name__} id {model_id} is invalid"}, 400))


    # returns task with the corresponding task_id
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        abort(make_response({"msg": f"{cls.__name__} {model_id} not found."}, 404))

    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
        
    except KeyError as error:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    return {cls.__name__.lower(): new_model.to_dict()}, 201

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    
    if filters:
        order_by = getattr(cls, filters.get("order_by", "title"))
        if filters.get("sort") == "desc":
            query = query.order_by(db.desc(order_by))
        else:
            query = query.order_by(db.asc(order_by))
    
    models = db.session.scalars(query)
    models_response = [model.to_dict() for model in models]

    return models_response