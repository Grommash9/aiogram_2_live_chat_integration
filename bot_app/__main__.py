import json
import random

from aiogram import executor
from aiogram.dispatcher.webhook import get_new_configured_app
from aiohttp import web

from bot_app import config, utils
from bot_app.misc import dp, bot, routes, scheduler


async def on_startup(_dispatcher):
    if int(config.is_ssl):
        await bot.set_webhook(config.WEBHOOK_URL, certificate=open('/etc/nginx/ssl/nginx.crt', 'r'))
    else:
        await bot.set_webhook(config.WEBHOOK_URL)

    webhook_info = await bot.get_webhook_info()
    print(webhook_info)
    bot_data = await bot.get_me()
    print(bot_data)

    live_chat_webhooks_list = await utils.live_chat_api.webhook.get.list_webhooks()

    current_webhook_url = f"{config.WEBHOOK_HOST}/{config.ROUTE_URL}/new_message"
    live_chat_webhook_data = f'current live chat webhook: {current_webhook_url}'
    if current_webhook_url not in [webhook['url'] for webhook in live_chat_webhooks_list]:
        if len(live_chat_webhooks_list) > 3:
            await utils.live_chat_api.webhook.delete.unregister_webhook(random.choice(live_chat_webhooks_list)['id'])
        await utils.live_chat_api.webhook.setup.register_webhook(current_webhook_url)
        live_chat_webhook_data = f'new live chat webhook: {current_webhook_url}'


    for users in config.NOTIFY_USERS:
        try:
            message_text = f"<b>@{bot_data.username} has been launched on the webhook!</b>\n\n" \
                           f"{config.WEBHOOK_HOST}/{config.ROUTE_URL}/send_message?user_id={users}&message=message%20from%20web\n\n" \
                            f"<a href='{config.WEBHOOK_HOST}/{config.ROUTE_URL}/log_errors'>Error log</a>\n\n" \
                            f"<a href='{config.WEBHOOK_HOST}/{config.ROUTE_URL}/log_output'>Output log</a>\n\n" \
                            f"{str(webhook_info)}\n\n" \
                            f"{str(bot_data)}\n\n" \
                           f"{live_chat_webhook_data}"

            await bot.send_message(users, message_text)
        except Exception as e:
            print(e)


async def on_shutdown(_dispatcher):
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


def setup_bot(app: web.Application):
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)


if __name__ == '__main__':
    scheduler.start()
    if int(config.POLLING):
        executor.start_polling(dp, skip_updates=True)
    else:
        app = get_new_configured_app(dispatcher=dp, path=f'/{config.WEBHOOK_PATH}/')
        app.add_routes(routes)
        setup_bot(app)
        web.run_app(app, **config.BOT_SERVER)

