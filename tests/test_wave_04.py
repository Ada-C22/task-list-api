from app.models.task import Task
import os

# There are no tests for wave 4.

# def test_massage_in_slack_on_completed_task(client, completed_task):
#     os.environ["SEND_SLACK_NOTIFICATIONS"] = "True"
    
#     # Act
#     response = client.patch(f"/tasks/1/mark_complete")
#     response_body = response.get_json()

#     # Assert
#     assert response.status_code == 200
#     assert response_body["task"]["is_complete"] == True
#     assert response_body == {
#         "task": {
#             "id": 1,
#             "title": "Go on my daily walk 🏞",
#             "description": "Notice something new every day",
#             "is_complete": True
#         }
#     }
#     assert Task.query.get(1).completed_at

#     # TODO somehow check that the message was posted in Slack channel.
#     # I haven't found Slack API method for that

#     os.environ["SEND_SLACK_NOTIFICATIONS"] = "False"
