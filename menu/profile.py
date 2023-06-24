from bot_create import bot
from aiogram import types
from auth_data import HOST, USER, PASSWORD, DB_NAME
import asyncpg


async def profile(message: types.Message):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    find_cash_user = await sql.fetch(f'SELECT cash FROM users WHERE id = {message.from_user.id};')
    await bot.send_message(message.from_user.id,
                           '📱 Ваш профиль:\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n🔑 Мой ID: <b>{0}</b>\n👤 Логин: @{1}'
                           '\n➖➖➖➖➖➖➖➖➖➖➖➖➖\n'
                           '💳 Баланс: <b>{2} рублей</b>'.
                           format(message.from_user.id, message.from_user.username, find_cash_user[0][0]),
                           parse_mode="html")
    await sql.close()
