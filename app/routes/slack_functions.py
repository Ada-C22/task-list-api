from flask import request, jsonify, abort, make_response
import requests
import os


def send_message(message, slack_channel, slack_url, slack_api_token):
    headers = { 
         'Authorization': f'Bearer {slack_api_token}',
         'Content-Type': 'application/json'
    }
    payload = {
        "channel": slack_channel,
        "text": message
        }   
        
    response = requests.post(slack_url, json=payload, headers= headers)
    if response.status_code != 200 or response.json().get("ok") is not True: 
        print("Failed to send Slack message: error unknown")

def send_message_with_config(message): 
        slack_channel = os.environ.get("SLACK_CHANNEL")
        slack_url = os.environ.get("SLACK_URL")
        slack_api_token = os.getenv("SLACK_BOT_TOKEN")

        return send_message(message, slack_channel, slack_url, slack_api_token)

    