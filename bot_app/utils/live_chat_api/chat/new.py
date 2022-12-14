import json
import aiohttp
from bot_app import config


async def create(customer_access_token):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({"continuous": True})

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/start_chat?organization_id={config.ORGANIZATION_ID}&continuous=True',
                                headers=headers, data=payload) as response:
            json_response = await response.json()

            return json_response
