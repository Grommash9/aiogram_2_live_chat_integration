'https://developers.livechat.com/docs/messaging/customer-chat-api#update-customer'

import json
import re

import aiohttp
import asyncio

from bot_app import config


async def update(customer_access_token, customer_full_name, photo_url):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
          "name": customer_full_name,
          "email": "t.anderson@example.com",
          "avatar": photo_url,
          "session_fields": [
            {
              "custom_key": "custom_value"
            },
            {
              "another_custom_key": "another_custom_value"
            }
          ]
        })

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/update_customer?organization_id={config.ORGANIZATION_ID}',
                                data=payload, headers=headers) as response:
            json_response = await response.json()

            print(json_response)




#
# loop = asyncio.get_event_loop()
# loop.run_until_complete(update('dal:YH4-T1nwTNW-wW8q8NDeVg'))