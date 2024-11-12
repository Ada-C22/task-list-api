from werkzeug.exceptions import HTTPException
from app.routes.route_utilities import validate_model
from app.models.task import Task
import pytest

def test_validate_model_id(one_task: None):
    # Act
    result_task = validate_model(Task, 1)

    # Assert
    assert result_task.id == 1
    assert result_task.title == "Go on my daily walk 🏞"
    assert result_task.description == "Notice something new every day"

def test_validate_model_missing_record(one_task: None):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_task = validate_model(Task,"3")
    
def test_validate_model_invalid_id(one_task: None):
    # Act & Assert
    # Calling `validate_model` without being invoked by a route will
    # cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_task = validate_model(Task,"cat")