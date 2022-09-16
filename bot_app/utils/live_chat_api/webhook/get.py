import json
import aiohttp
from bot_app import config


async def list_webhooks():
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
            "owner_client_id": config.CLIENT_ID
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Basic {config.BASE64_ENCODED}'
        }

        async with session.post(
                f'https://api.livechatinc.com/v3.4/configuration/action/list_webhooks',
                headers=headers, data=payload) as response:
            json_response = await response.json()
            return json_response
