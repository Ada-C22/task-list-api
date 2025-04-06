import os

import requests

from app.slack.slackmessage import SlackMessage


class SlackClient:
    def __init__(self):
        self.token = os.environ.get('SLACK_TOKEN')
        self.url = "https://slack.com/api"
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    def post_message(self, slack_message: SlackMessage):
        response = requests.post(f"{self.url}/chat.postMessage", headers=self.headers, json=slack_message.__dict__)
        return response.status_code == 200
