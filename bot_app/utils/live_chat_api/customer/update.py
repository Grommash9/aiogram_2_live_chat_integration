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
          "avatar": photo_url,
        })

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/update_customer?organization_id={config.ORGANIZATION_ID}',
                                data=payload, headers=headers) as response:
            json_response = await response.json()


async def update_email(customer_access_token, email):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
          "email": email,
        })

        headers = {
          'Content-Type': 'application/json',
          'Authorization': f'Bearer {customer_access_token}'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/update_customer?organization_id={config.ORGANIZATION_ID}',
                                data=payload, headers=headers) as response:
            json_response = await response.json()
