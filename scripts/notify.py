import requests
import json
from dotenv import dotenv_values

config = dotenv_values("../.env")
SLACK_WEBHOOK_URL = config.get("SLACK_WEBHOOK_URL", "")


def send_notification(message):
    payload = {"text": message}

    response = requests.post(
        SLACK_WEBHOOK_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
    )
    
    if response.status_code != 200:
        raise Exception(f"Slack webhook failed: {response.status_code}, {response.text}")

    return response.text

