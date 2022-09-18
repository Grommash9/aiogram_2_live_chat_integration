import json
import os
import pathlib
from io import BytesIO
from urllib.parse import unquote
import aiohttp
from aiohttp.web_routedef import Request
from bot_app import config, db
from aiohttp import web
from bot_app.misc import routes, bot, redis

@routes.post(f'/{config.ROUTE_URL}/new_message')
async def get_live_chat_event(request: Request):

    bytes_req_data = await request.content.read()

    data = json.loads(bytes_req_data.decode())

    event = data['payload'].get('event')
    if event is None:
        return



    message_from_user = await db.users.get_user_by_entity_id(event['author_id'])
    if message_from_user is not None:
        return

    chat_id = data['payload'].get('chat_id')

    if chat_id is None:
        return

    silent = await redis.get(event["id"])
    if silent is not None:
        return

    chat_data = await db.telegram_chat_id_live_chat_id.get_chat_by_lc(chat_id)

    if event['type'] == 'message':
        try:
            await bot.send_message(chat_data['telegram_chat_id'],
                                   data['payload']['event'].get('text'))
        except TypeError:
            print('chat not found', chat_id)

    if event['type'] == 'file':
        if event['content_type'] in ['image/jpeg', 'image/png', 'image/bmp']:
            try:
                await bot.send_photo(chat_data['telegram_chat_id'],
                                     event['url'])
            except TypeError:
                print('chat not found', chat_id)
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(event['url']) as resp:
                    data = await resp.read()

            bio = BytesIO()
            bio.write(data)
            bio.name = unquote(event['url']).split('/')[-1]

            bio.seek(0)

            await bot.send_document(chat_data['telegram_chat_id'],
                                    document=bio)
    return web.Response(status=200, body='message sent')


@routes.get(f'/{config.ROUTE_URL}/send_message')
async def get_handler(request):
    tx_data = dict(request.query)
    message_text = tx_data['message']
    user_id = tx_data['user_id']

    try:
        await bot.send_message(user_id, message_text)
    except Exception as e:
        return web.Response(status=404, body=str(e))
    return web.Response(status=200, body='ok')


@routes.get(f"/{config.ROUTE_URL}/log_errors")
async def get_errors(request):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'log_error.log'), 'r') as error_file:
            data = error_file.read()
        return web.Response(status=200, body=data)
    except Exception as e:
        return web.Response(status=404, body=str(e))


@routes.get(f"/{config.ROUTE_URL}/log_output")
async def get_errors(request):
    try:
        with open(os.path.join(pathlib.Path(__file__).parent.parent.parent.resolve(), 'log_output.log'), 'r') as error_file:
            data = error_file.read()
        return web.Response(status=200, body=data)
    except Exception as e:
        return web.Response(status=404, body=str(e))
