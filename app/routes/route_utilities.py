from flask import abort, make_response, request
from ..db import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} id {model_id} invalid"}, 400))
    
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model

def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except KeyError:
        response = {"details": f"Invalid data"}
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()
    return {f"{cls.__name__.lower()}": new_model.to_dict()}, 201

def delete_model(cls, model_id):
    model = validate_model(cls, model_id)    
    db.session.delete(model)
    db.session.commit()
    return {"details": f"{cls.__name__} {model_id} \"{model.title}\" successfully deleted"}

def get_models_with_query_params(cls, filters=None):
    query = db.select(cls)
    
    if filters:
        for attribute, value in filters.items():
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    sort_by = request.args.get("sort_by", "title")
    sort_order = request.args.get("sort", "asc")
    if sort_by and hasattr(cls, sort_by):
        if sort_order == "desc":
            query = query.order_by(getattr(cls, sort_by).desc())
        else:
            query = query.order_by(getattr(cls, sort_by))
    else:
        query = query.order_by(cls.id)
    
    models = db.session.scalars(query)
    return [model.to_dict() for model in models]
