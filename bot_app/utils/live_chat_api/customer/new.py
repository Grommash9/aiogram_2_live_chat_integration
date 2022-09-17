import json
import re

import aiohttp
import asyncio

from bot_app import config


async def create():
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
          "grant_type": "cookie",
          "client_id": config.CLIENT_ID,
          "license_id": config.LICENSE_ID,
          "redirect_uri": "https://livechat.cool/"
        })

        headers = {
            'Content-Type': 'application/json',
        }

        async with session.post('https://accounts.livechat.com/customer/token', data=payload, headers=headers) as response:
            json_response = await response.json()

            lc_cid_results = re.findall(r'__lc_cid=([0-9a-z-]+);', response.cookies.output())
            lc_cst_results = re.findall(r'__lc_cst=([0-9a-z]+);', response.cookies.output())

            data = {'access_token': json_response['access_token'],
                    'lc_cid': lc_cid_results[0],
                    'lc_cst': lc_cst_results[0],
                    'entity_id': json_response['entity_id']}

            return data




