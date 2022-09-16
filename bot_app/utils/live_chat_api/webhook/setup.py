import json
import aiohttp
from bot_app import config


async def register_webhook(new_webhook_url, description='basic telegram bot token', action='incoming_event'):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
            "url": new_webhook_url,
            "description": description,
            "action": action,
            "secret_key": config.WEBHOOK_SECRET_CODE,
            "owner_client_id": config.CLIENT_ID,
            "type": "license"
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {config.BASE64_ENCODED}'
        }

        async with session.post(
                f'https://api.livechatinc.com/v3.4/configuration/action/register_webhook',
                headers=headers, data=payload) as response:
            json_response = await response.json()
            return json_response
