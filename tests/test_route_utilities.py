import pytest
from app.models.task import Task
from app.models.goal import Goal
from app.routes.route_utilities import validate_new_model_data, get_models_with_filters

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_validate_new_model_data():
    # Arrrange & 
    model_data = {"title": "New ADA task", "description": "Making a new model"}
    cls = Task
    # Act
    results = validate_new_model_data(cls, model_data)

    # Assert
    assert results == model_data


# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_models_with_filters(three_tasks):
    # Arrange
    cls = Task
    filter_params = {
        "title": "water"
    }

    # Act
    result = get_models_with_filters(cls, filter_params)

    # Assert
    assert result[1] == 200
    assert len(result[0]) == 1
    assert result[0] == [{
        "id": 1,
        "title": "Water the garden 🌷", 
        "description": "", 
        "is_complete": False}]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_models_with_filters_no_filter_params(three_tasks):
    # Arrange
    cls = Task
    # Act
    result = get_models_with_filters(cls)

    # Assert
    assert result[1] == 200
    assert len(result[0]) == 3
    assert result[0] == [
        {
            "id": 1,
            "title": "Water the garden 🌷", 
            "description": "", 
            "is_complete": False
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧", 
            "description":"", 
            "is_complete": False
        },
        {
            "id": 3,
            "title":"Pay my outstanding tickets 😭", 
            "description":"", 
            "is_complete": False
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_models_with_filters_order_by(three_tasks):
    # Arrange
    cls = Task
    filter_params = {"order_by": "title"}
    # Act
    result = get_models_with_filters(cls, filter_params)

    # Assert
    assert result[1] == 200
    assert len(result[0]) == 3
    assert result[0] == [
        {
            "id": 2,
            "title": "Answer forgotten email 📧", 
            "description":"", 
            "is_complete": False
        },
        {
            "id": 3,
            "title":"Pay my outstanding tickets 😭", 
            "description":"", 
            "is_complete": False
        },
        {
            "id": 1,
            "title": "Water the garden 🌷", 
            "description": "", 
            "is_complete": False
        }
    ]

# @pytest.mark.skip(reason="No way to test this feature yet")
def test_get_models_with_filters_sort_desc(three_tasks):
    # Arrange
    cls = Task
    filter_params = {"sort": "desc"}
    # Act
    result = get_models_with_filters(cls, filter_params)

    # Assert
    assert result[1] == 200
    assert len(result[0]) == 3
    assert result[0] == [
        {
            "id": 1,
            "title": "Water the garden 🌷", 
            "description": "", 
            "is_complete": False
        },
        {
            "id": 3,
            "title":"Pay my outstanding tickets 😭", 
            "description":"", 
            "is_complete": False
        },
        {
            "id": 2,
            "title": "Answer forgotten email 📧", 
            "description":"", 
            "is_complete": False
        }
    ]