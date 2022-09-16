import aiogram.types
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from bot_app import db, markups
from bot_app.misc import bot, dp
from bot_app.utils import live_chat_api
from bot_app import utils


@dp.message_handler(commands='start', state='*')
async def process_start(message: Message, state: FSMContext):
    await db.users.create_user(message.from_user, message.get_args())
    await state.finish()
    await bot.send_message(message.from_user.id,
                           'basic hello message',
                           reply_markup=markups.user.main.main_menu())


@dp.message_handler()
async def new_message(message: Message):
    user_access_token = await utils.live_chat_api.user_access_token.get(message.from_user)
    live_chat_id = await utils.live_chat_api.chat.get.live_chat_id(message.from_user.id,
                                                                   user_access_token)

    await utils.live_chat_api.chat.resume_chat.resume(user_access_token, live_chat_id)

    await live_chat_api.message.send.send(customer_access_token=user_access_token,
                                          live_chat_id=live_chat_id,
                                          message_text=message.text)

    await bot.send_message(message.from_user.id,
                           'dadad')

    await utils.live_chat_api.agent.message.send(live_chat_id, 'dadad')


@dp.message_handler(content_types=aiogram.types.ContentTypes.PHOTO)
async def get_photo(message: Message):
    print(message)
    photo_file = await bot.get_file(message.photo[-1].file_id)
    file_id = photo_file.file_id
    file_name = photo_file.file_path.split('/')[-1]

    image_path = rf'C:\Users\Гриша\PycharmProjects\aiogram_2_live_chat_integration\bot_app\handlers\user\{file_name}'

    data = await bot.download_file(photo_file.file_path, image_path)
    print(data)



    user_access_token = await utils.live_chat_api.user_access_token.get(message.from_user)


    await utils.live_chat_api.message.send.send_photo(user_access_token, file_name, image_path)
