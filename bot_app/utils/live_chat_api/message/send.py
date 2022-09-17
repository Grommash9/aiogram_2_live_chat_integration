import asyncio

import aiohttp
import json
from bot_app import config


async def send(customer_access_token, live_chat_id, message_text):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
            "chat_id": live_chat_id,
            "event": {
                "type": "message",
                "text": message_text,
                "recipients": "all"
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/send_event?organization_id={config.ORGANIZATION_ID}',
                                headers=headers, data=payload) as response:
            json_response = await response.json()

            print(json_response)


async def send_file(customer_access_token, live_chat_id, file_url):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
            "chat_id": live_chat_id,
            "event": {
                "type": "file",
                "url": file_url,
            }
        })

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/send_event?organization_id={config.ORGANIZATION_ID}',
                                headers=headers, data=payload) as response:
            json_response = await response.json()

            print(json_response)
