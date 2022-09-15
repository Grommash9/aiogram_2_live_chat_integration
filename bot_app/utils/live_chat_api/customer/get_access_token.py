import json
import re

import aiohttp
import asyncio

from bot_app import config


async def get(lc_cid, lc_cst):
    async with aiohttp.ClientSession() as session:
        payload = json.dumps({
          "grant_type": "cookie",
          "client_id": config.CLIENT_ID,
          "license_id": config.LICENSE_ID,
          "redirect_uri": "https://livechat.cool/"
        })
        headers = {
          'Content-Type': 'application/json'
        }

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'__lc_cid={lc_cid}; '
                      f'__lc_cst={lc_cst};'
        }

        async with session.post('https://accounts.livechat.com/customer/token', data=payload, headers=headers) as response:
            json_response = await response.json()

            lc_cid_results = re.findall(r'__lc_cid=([0-9a-z-]+);', response.cookies.output())
            lc_cst_results = re.findall(r'__lc_cst=([0-9a-z]+);', response.cookies.output())

            data = {'access_token': json_response['access_token'],
             'lc_cid': lc_cid_results[0],
             'lc_cst': lc_cst_results[0]}

            print(data)



# loop = asyncio.get_event_loop()
# loop.run_until_complete(get('76cd9f3d-c610-4d35-5ee0-46f0ba444649', '8be68f9a51de0c22e39d53b820fad69632d5f5560a7eca34522632334e9fa3c85492b7c516e0e75796279a317ebafbd5c746925d7022cbd425bbbc79549e'))
#

