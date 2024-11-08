from flask import abort, make_response
from ..db import db

def validate_model(cls, model_id):
    model_prefix = 'goal' if cls.__name__.lower() == 'goal' else 'task'
    
    try:
        model_id = int(model_id)
    except ValueError:
        abort(make_response({"message": f"{model_prefix}_id {model_id} invalid"}, 400))
    
    # query = db.select(cls).where(cls.id == model_id)
    # model = db.session.scalar(query)
    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{model_prefix}_id {model_id} not found"}, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError as error:
        response = {"message": f"Invalid request: missing {error.args[0]}"}
        abort(make_response(response, 400))

def get_model_with_filters(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if isinstance(value, list):
                    query = query.where(getattr(cls, attribute).in_(value))
            else:
                    query = query.where(getattr(cls, attribute).ilike(f"%{value}%") if isinstance(value, str) else getattr(cls, attribute) == value)
    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]

    return models_response       