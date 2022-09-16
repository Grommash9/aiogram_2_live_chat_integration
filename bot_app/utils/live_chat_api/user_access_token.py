from aiogram.types import User

from bot_app.misc import redis, bot
from bot_app import db, utils, config


async def get(user: User):
    access_token = await redis.get(f'access-token_{user.id}')
    if access_token is not None:
        return access_token

    user_data = await db.users.get_user(user.id)

    if user_data['live_chat_cid'] is not None and user_data['live_chat_cst'] is not None:
        user_access_data = await utils.live_chat_api.customer.get_access_token.get(user_data['live_chat_cid'],
                                                                                   user_data['live_chat_cst'])
        await redis.set(f'access-token_{user.id}', user_access_data['access_token'], 21600)
        return user_access_data['access_token']

    access_token = await utils.live_chat_api.create_user.new(user)

    await redis.set(f'access-token_{user.id}', access_token, 21600)
    return access_token
