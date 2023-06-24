from bot_create import bot, Dispatcher
from aiogram import types
from keyboards import kb_reg, kb_main
from handlers.mainMenu import main
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


async def startup(message: types.Message):  # Здороваемся
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    find_row_user = await sql.fetch(f'SELECT id FROM users WHERE id = {message.from_user.id};')
    if str(find_row_user) == '[]':
        await bot.send_message(message.from_user.id,
                               "Добро пожаловать!"
                               "\nЯ - GodSeo | Bot, и я помогу поднять SEO на твоих видеороликах. "
                               "Перед тем, как начать работу нужно согласиться с правилами:"
                               "\nhttps://telegra.ph/Pravilo-bota-GodSeo-bot-09-27",
                               parse_mode="html", reply_markup=kb_reg)
        await registration(message)
    else:
        await message.answer('<b>Главное меню бота</b>', reply_markup=kb_main, parse_mode="html")


async def registration(message: types.Message):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    if message.text == 'Да':
        await sql.execute(
            f"""INSERT INTO users (username, id, cash, pay_id, promocode)
            VALUES ('{message.from_user.username}', '{message.from_user.id}', '0', '0', '0')""")
        await bot.send_message(message.from_user.id,
                               '<b>Вы согласились с правилами! Доступ к боту открыт.</b>',
                               parse_mode="html", reply_markup=kb_main)
        await sql.close()
        await main(message)
    else:
        await message.answer('<b>Для продолжения нужно согласиться с правилами! Вы согласны?</b>', parse_mode="html")


def register_handler_startup(dp: Dispatcher):
    dp.register_message_handler(startup, commands=['start'])
    dp.register_message_handler(registration, content_types=['text'], text='Да')
