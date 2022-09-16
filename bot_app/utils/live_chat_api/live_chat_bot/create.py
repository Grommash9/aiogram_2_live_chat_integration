async def create_bot():
    import requests
    import json

    url = "https://api.livechatinc.com/v3.4/configuration/action/create_bot"

    payload = json.dumps({
        "name": "First Agent",
        "owner_client_id": "2faa1a37330c691f77a4ef253a30be26"
    })
    headers = {
        'Authorization': 'Basic ODZhNzBkZTQtNmM1MC00NmYyLTkyN2UtNzMwNzg2ZTZiZWFhOmRhbDpWRVZKQ3dOQzRYQS1OLUNiNHRhT3lnX0JyWGM=',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

