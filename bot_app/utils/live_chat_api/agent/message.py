import aiohttp
import json
from bot_app import config


async def send(chat_id, message_text):

    url = "https://api.livechatinc.com/v3.4/agent/action/send_event"

    payload = json.dumps({
        "chat_id": chat_id,
        "event": {
            "type": "message",
            "text": message_text,
            "visibility": "all"
        }
    })
    headers = {
        'Authorization': f'Basic {config.BASE64_ENCODED}',
        'Content-Type': 'application/json'
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(url,
                                headers=headers, data=payload) as response:
            json_response = await response.json()

            return json_response