import aiohttp

import json

from bot_app import config


async def resume(customer_access_token, chat_id):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
            "chat": {
                "id": chat_id
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(
                f'https://api.livechatinc.com/v3.4/customer/action/resume_chat?organization_id={config.ORGANIZATION_ID}',
                headers=headers, data=payload) as response:
            json_response = await response.json()

            return json_response
