import requests
from bot_app import config
from bot_app.utils import async_to_sync


def sync_upload_file(customer_access_token, file, file_name, file_type):
    headers = {
        'Authorization': f'Bearer {customer_access_token}',
    }

    params = {
        'organization_id': config.ORGANIZATION_ID,
    }

    files = {
        ('file', (file_name, file, file_type))
    }

    response = requests.post('https://api.livechatinc.com/v3.4/customer/action/upload_file', params=params,
                             headers=headers, files=files)

    return response.json()


async def async_file_upload(customer_access_token, file, file_name, file_type):
    data = await async_to_sync.run_blocking_io(sync_upload_file, customer_access_token, file, file_name, file_type)
    return data

