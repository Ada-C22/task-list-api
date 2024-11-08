from flask import abort, make_response
from app import db

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"error": f"{cls.__name__} {model_id} invalid"}
        abort(make_response(response, 400))

    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)
    
    if not model: 
        response = {"error": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model

def create_model(cls, model_data):
    try: 
        new_model = cls.from_dict(model_data)

    except KeyError as error: 
        response = {"error": f"Invalid request: missing {error.args[0]}"}        
        abort(make_response(response, 400))
    
    db.session.add(new_model)
    db.session.commit()

    dict=cls.to_dict(new_model)

    response = {((cls.__name__).lower()):dict}
    return(make_response(response,201))

def get_models_with_filters(cls, filters=None):
    query = db.select(cls)
    if filters:
        for attribute, value in filters.items():
            if hasattr(cls,attribute): 
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    models = db.session.scalars(query.order_by(cls.id))
    models_response = [model.to_dict() for model in models]
    return models_response            


def delete_model(cls,model):
    model_id = model.id
    model_title = model.title

    db.session.delete(model)
    db.session.commit()

    details = f"{cls.__name__} {model_id} \"{model_title}\" successfully deleted"
    response_body = {"details": details}
    return response_body

def check_for_completion(cls, model):
    completed_at = model.completed_at
    if completed_at is None:
        return False
    else: 
        return True