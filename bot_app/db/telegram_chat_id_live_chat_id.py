import datetime

from aiogram.types import User

from bot_app.db.base import create_dict_con


async def create_chat_connection(telegram_chat_id, live_chat_chat_id):
    con, cur = await create_dict_con()
    await cur.execute('insert ignore into telegram_chat_id_live_chat_id (telegram_chat_id, live_chat_chat_id) '
                      'values (%s, %s)',
                      (telegram_chat_id, live_chat_chat_id))
    await con.commit()
    await con.ensure_closed()



async def get_chat_by_tg(telegram_chat_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from telegram_chat_id_live_chat_id where telegram_chat_id = %s ', (telegram_chat_id,))
    chat_data = await cur.fetchone()
    await con.ensure_closed()
    return chat_data


async def get_chat_by_lc(live_chat_chat_id):
    con, cur = await create_dict_con()
    await cur.execute('select * from telegram_chat_id_live_chat_id where live_chat_chat_id = %s ', (live_chat_chat_id,))
    chat_data = await cur.fetchone()
    await con.ensure_closed()
    return chat_data
