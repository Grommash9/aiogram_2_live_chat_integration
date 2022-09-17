import aiogram.types
import aiohttp
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from bot_app import db, markups
from bot_app.misc import bot, dp
from bot_app.utils import live_chat_api
from bot_app import utils
from io import BytesIO


@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    await db.users.create_user(message.from_user, message.get_args())
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'basic hello message',
                           reply_markup=markups.user.main.main_menu())

@dp.message_handler(commands=['get'])
async def get_file(message: Message):
    url = 'https://cdn.livechat-files.com/api/file/lc/att/14516034/c8ae674e4a320af3e21e6b91d60b68f6/file_1%20%281%29.xlsx'


    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.read()


    bio = BytesIO()
    bio.write(data)
    bio.name = 'daa.xlsx'
    bio.seek(0)


    await bot.send_document(message.from_user.id, bio)




@dp.message_handler()
async def new_message(message: Message):
    user_access_token = await utils.live_chat_api.user_access_token.get(message.from_user)
    live_chat_id = await utils.live_chat_api.chat.get.live_chat_id(message.from_user.id,
                                                                   user_access_token)

    await utils.live_chat_api.chat.resume_chat.resume(user_access_token, live_chat_id)

    await live_chat_api.message.send.send(customer_access_token=user_access_token,
                                          live_chat_id=live_chat_id,
                                          message_text=message.text)

    # await bot.send_message(message.from_user.id,
    #                        'dadad')
    #
    # await utils.live_chat_api.agent.message.send(live_chat_id, 'dadad')


@dp.message_handler(content_types=aiogram.types.ContentTypes.PHOTO)
async def get_photo(message: Message):

    photo_file = await bot.get_file(message.photo[-1].file_id)

    user_access_token = await utils.live_chat_api.user_access_token.get(message.from_user)

    live_chat_id = await utils.live_chat_api.chat.get.live_chat_id(message.from_user.id,
                                                                   user_access_token)

    await utils.live_chat_api.chat.resume_chat.resume(user_access_token, live_chat_id)

    bio = BytesIO()
    await bot.download_file_by_id(photo_file.file_id, bio)
    bio.seek(0)

    file_name = photo_file.file_path.split('/')[-1]
    file_live_chat_data = await utils.live_chat_api.files.upload.async_file_upload(user_access_token, bio, file_name,
                                                                                   f'image/{file_name.split(".")[-1]}')

    await utils.live_chat_api.message.send.send_file(user_access_token, live_chat_id, file_live_chat_data['url'])


@dp.message_handler(content_types=aiogram.types.ContentTypes.DOCUMENT)
async def get_document_type(message: Message):
    user_access_token = await utils.live_chat_api.user_access_token.get(message.from_user)

    bio = BytesIO()
    await bot.download_file_by_id(message.document.file_id, bio)
    bio.seek(0)

    file_live_chat_data = await utils.live_chat_api.files.upload.async_file_upload(user_access_token,
                                                                                   bio, message.document.file_name,
                                                                                   message.document.mime_type)

    live_chat_id = await utils.live_chat_api.chat.get.live_chat_id(message.from_user.id,
                                                                   user_access_token)

    await utils.live_chat_api.chat.resume_chat.resume(user_access_token, live_chat_id)

    await utils.live_chat_api.message.send.send_file(user_access_token, live_chat_id, file_live_chat_data['url'])


