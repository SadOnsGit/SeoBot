from aiogram.utils import executor
from bot_create import dp
from handlers import registration, mainMenu, admin, create_promocode
from callback import seostatus, purchase_crystal, zaliv, promocodes, cancel_seo_send
from database import create_db

registration.register_handler_startup(dp)
create_promocode.register_handlers_promocode(dp)
admin.register_handlers_admin(dp)
mainMenu.register_handler_menu(dp)
cancel_seo_send.register_cancel_btn(dp)
seostatus.register_callback_status_seo(dp)
purchase_crystal.register_callback_crystal(dp)
zaliv.register_callback_zaliv(dp)
promocodes.registration_function_promocodes(dp)


async def on_startup(_):
    await create_db.create_bot_database()
    print('Бот успешно запущен!\nSEO BOT by SADONS')


executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
