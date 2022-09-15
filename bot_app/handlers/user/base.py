import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram import types


from bot_app import db, markups, config
from bot_app.misc import bot, dp, redis
from bot_app.states.user import User
from bot_app.utils import live_chat_api
from aiogram.types import PhotoSize
import abc



@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    user_data = await db.users.create_user(message.from_user, message.get_args())
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'basic hello message',
                           reply_markup=markups.user.main.main_menu())


@dp.message_handler(commands='photo')
async def setup_photo(message: Message):
    profile_photos = await message.from_user.get_profile_photos(limit=1)
    print(data)
    print(data.photos[-1][-1].file_id)
    file_data = await bot.get_file(data.photos[-1][-1].file_id)
    print(file_data)

    file_data['file_path']

    file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_data['file_path']}"







@dp.message_handler()
async def new_message(message: Message):
    user_access_token = await redis.get(str(message.from_user.id))

    if user_access_token is not None:

        chat_data = await db.telegram_chat_id_live_chat_id.get_chat_by_tg(message.chat.id)
        print(chat_data)

        await live_chat_api.message.send.send(customer_access_token=user_access_token,
                                              live_chat_id=chat_data['live_chat_chat_id'],
                                              message_text=message.text)
        return
    customer_data = await live_chat_api.customer.new.create()
    print(customer_data)

    await db.users.add_live_chat_cookie_data(message.from_user.id,
                                             customer_data['lc_cid'],
                                             customer_data['lc_cst'])

    profile_photos = await message.from_user.get_profile_photos(limit=1)
    try:
        file_data = await bot.get_file(profile_photos.photos[-1][-1].file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_data['file_path']}"
    except IndexError:
        file_url = f"https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg"

    await live_chat_api.customer.update.update(customer_data['access_token'],
                                               customer_full_name=message.from_user.full_name,
                                               photo_url=file_url)



    chat_data = await live_chat_api.chat.new.create(customer_data['access_token'])

    print(chat_data)

    live_chat_chat_id = chat_data['chat_id']

    await db.telegram_chat_id_live_chat_id.create_chat_connection(message.chat.id,
                                                                  live_chat_chat_id)

    user_access_token = customer_data['access_token']

    await redis.set(str(message.from_user.id), customer_data['access_token'])

    await live_chat_api.message.send.send(customer_access_token=user_access_token,
                                          live_chat_id=live_chat_chat_id,
                                          message_text=message.text)

