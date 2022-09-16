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


async def send_photo(customer_access_token, file_name, file_path):
    async with aiohttp.ClientSession() as session:
        payload = {}
        files = [
            ('file', (
            file_name, open(file_path, 'rb'), 'image/gif'))
        ]

        headers = {
            'Authorization': f'Bearer {customer_access_token}',
            'Content-Type': 'multipart/form-data; boundary=--------------------------210197025774705439685896',
            'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
        }

        async with session.post(f'https://api.livechatinc.com/v3.4/customer/'
                                f'action/upload_file?organization_id={config.ORGANIZATION_ID}',
                                headers=headers, data=payload, files=files) as response:
            json_response = await response.json()

            print(json_response)


def sync_send_photo(customer_access_token, file_name, file_path):
    import requests

    url = f"https://api.livechatinc.com/v3.4/customer/action/upload_file?organization_id={config.ORGANIZATION_ID}"

    payload = {}
    files = [
        ('file', (file_name, open(
            file_path, 'rb').read(),
                  'image/jpeg'))
    ]
    print(files)
    headers = {
        'Authorization': f'Bearer {customer_access_token}',
        'Content-Type': 'multipart/form-data; boundary=--------------------------210197025774705439685896',
        'Content-Type': 'multipart/form-data; boundary=----WebKitFormBoundary7MA4YWxkTrZu0gW'
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    print(response.text)

data = open(r'C:\Users\Гриша\PycharmProjects\aiogram_2_live_chat_integration\bot_app\handlers\user\file_2.jpg', 'rb')
print(data.read())

sync_send_photo('dal:S8-PVaCDT2qAv2qWzUA1fg', 'file_2.jpg', r'C:\Users\Гриша\PycharmProjects\aiogram_2_live_chat_integration\bot_app\handlers\user\file_2.jpg')