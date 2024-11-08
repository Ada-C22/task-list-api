import os
import requests

SLACK_CHANNEL = "task-notifications"
SLACK_BASE_URL = "https://slack.com/api/chat.postMessage"

def send_slack_message(task_title):
    slack_token = os.environ.get("SLACK_API_TOKEN")

    if not slack_token:
        return "Slack API token not found"
    
    message = f"Someone just completed the task: {task_title}"

    headers = {
        "Authorization": f"Bearer {slack_token}",
        "Content-Type": "application/json"
    }

    notification = {
        "channel": SLACK_CHANNEL,
        "text": message
    }

    response = requests.post(SLACK_BASE_URL, json=notification, headers=headers)

    if response.status_code != 200:
        return (f"Failed to send Slack Message: {response.status_code}, {response.text}")