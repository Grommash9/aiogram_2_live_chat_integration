from bot_app import utils, db, config
from bot_app.misc import bot


async def new(user):
    customer_data = await utils.live_chat_api.customer.new.create()

    await db.users.add_live_chat_cookie_data(user.id,
                                             customer_data['lc_cid'],
                                             customer_data['lc_cst'],
                                             customer_data['entity_id'])

    profile_photos = await user.get_profile_photos(limit=1)
    try:
        file_data = await bot.get_file(profile_photos.photos[-1][-1].file_id)
        file_url = f"https://api.telegram.org/file/bot{config.BOT_TOKEN}/{file_data['file_path']}"
    except IndexError:
        file_url = f"https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg"

    await utils.live_chat_api.customer.update.update(customer_data['access_token'],
                                                     customer_full_name=user.full_name,
                                                     photo_url=file_url)
    return customer_data['access_token']
