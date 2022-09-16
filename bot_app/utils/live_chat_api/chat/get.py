from bot_app import db, utils
from bot_app.misc import redis


async def live_chat_id(telegram_chat_id, access_token):
    live_chat_id = await redis.get(f'tg-chat-to-live-chat_{telegram_chat_id}')

    if live_chat_id is not None:
        return live_chat_id

    chat_data = await db.telegram_chat_id_live_chat_id.get_chat_by_tg(telegram_chat_id)
    if chat_data is not None:
        await redis.set(f'tg-chat-to-live-chat_{telegram_chat_id}', chat_data['live_chat_chat_id'])
        return chat_data['live_chat_chat_id']

    new_chat_data = await utils.live_chat_api.chat.new.create(access_token)

    await db.telegram_chat_id_live_chat_id.create_chat_connection(telegram_chat_id, new_chat_data['chat_id'])

    await redis.set(f'tg-chat-to-live-chat_{telegram_chat_id}', new_chat_data['chat_id'])
    return new_chat_data['chat_id']
