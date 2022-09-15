import json
import os
import pathlib

from aiohttp.web_routedef import Request

from bot_app import config, db
from aiohttp import web

from bot_app.misc import routes, bot


@routes.post(f'/{config.ROUTE_URL}/new_message')
async def get_live_chat_event(request: Request):
    tx_data = dict(request.query)


    bytes_req_data = await request.content.read()

    data = json.loads(bytes_req_data.decode())

    print(json.dumps(data['payload'], indent=4))

    chat_id = data['payload'].get('chat_id')



    if data['payload']['event']['author_id'] != 'andreevichprudnikov@gmail.com':
        return

    if chat_id is not None:
        chat_data = await db.telegram_chat_id_live_chat_id.get_chat_by_lc(chat_id)
        try:
            await bot.send_message(chat_data['telegram_chat_id'],
                                   data['payload']['event'].get('text'))
        except TypeError:
            print('chat not found', chat_id)

    return web.Response(status=200, body='ok')




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