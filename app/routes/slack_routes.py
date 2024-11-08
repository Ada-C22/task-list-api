from flask import Blueprint, request, jsonify
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import os

# Initialize the Blueprint
slack_bp = Blueprint('slack_bp', __name__)

# Slack Bot Token from environment variable
SLACK_BOT_TOKEN ="n/a"
client = WebClient(token=SLACK_BOT_TOKEN)

@slack_bp.post('/send_message')
def send_message():
    data = request.get_json()
    channel = data.get("channel")
    message = data.get("message")

    if not channel or not message:
        return jsonify({"error": "Channel and message are required"}), 400

    try:
        # Make the chat.postMessage API call
        response = client.chat_postMessage(channel=channel, text=message)
        return jsonify({"ok": response["ok"], "message": "Message sent successfully!"}), 200
    except SlackApiError as e:
        # Handle Slack API error and print more details for debugging
        error_message = e.response["error"]
        print(f"Slack API Error: {error_message}")
        return jsonify({"ok": False, "error": error_message}), 400
    app.run(debug=True)


