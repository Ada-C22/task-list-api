from app.models.task import Task
import pytest

def test_from_dict_returns_model():
    # Arrange
    model_data = {
        "title": "New Test Task",
        "description": "something new to do"
    }

    # Act
    new_model = Task.from_dict(model_data)

    # Assert
    assert new_model.title == "New Test Task"
    assert new_model.description == "something new to do"

def test_from_dict_with_no_title():
    # Arrange
    model_data = {
        "description": "something new to do"
    }

    # Act & Assert
    with pytest.raises(KeyError, match = 'title'):
        new_model = Task.from_dict(model_data)

def test_from_dict_with_no_description():
    # Arrange
    model_data = {
        "title": "New Test Task"
    }

    # Act & Assert
    with pytest.raises(KeyError, match = 'description'):
        new_model = Task.from_dict(model_data)

def test_from_dict_with_extra_keys():
    # Arrange
    model_data = {
        "extra": "some stuff",
        "title": "New Test Task",
        "description": "something new to do",
        "another": "last value"
    }

    # Act
    new_model = Task.from_dict(model_data)

    # Assert
    assert new_model.title == "New Test Task"
    assert new_model.description == "something new to do"

def test_to_dict_no_missing_data():
    # Arrange
    test_data = Task(id = 1,
                    title="Test Task",
                    description="test description task")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result["task"]) == 4
    assert result["task"]["id"] == 1
    assert result["task"]["title"] == "Test Task"
    assert result["task"]["description"] == "test description task"
    assert "task" in result

def test_to_dict_missing_id():
    # Arrange
    test_data = Task(title="Test Task",
                    description="test description task")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result["task"]) == 4
    assert result["task"]["id"] is None
    assert result["task"]["title"] == "Test Task"
    assert result["task"]["description"] == "test description task"

def test_to_dict_missing_title():
    # Arrange
    test_data = Task(id=1,
                    description="test description task")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result["task"]) == 4
    assert result["task"]["id"] == 1
    assert result["task"]["title"] is None
    assert result["task"]["description"] == "test description task"

def test_to_dict_missing_description():
    # Arrange
    test_data = Task(id = 1,
                    title="Test Task")

    # Act
    result = test_data.to_dict()

    # Assert
    assert len(result["task"]) == 4
    assert result["task"]["id"] == 1
    assert result["task"]["title"] == "Test Task"
    assert result["task"]["description"] is None