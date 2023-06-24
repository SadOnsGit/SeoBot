from bot_create import dp, bot
from callback.zaliv import Zaliv
from aiogram import types
from aiogram.dispatcher import FSMContext
from keyboards.kb_zaliv import kb_zaliv_status
from auth_data import ZALIV_CHAT_ID
import re
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


@dp.message_handler(state=Zaliv.link)
async def zaliv_create_exp(message: types.Message, state: FSMContext):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    usercash = await sql.fetch(f"SELECT cash FROM users WHERE id = '{message.chat.id}'")
    try:
        if usercash[0][0] >= 50:
            link = re.search(r"(?P<url>https?://\S+)", message.text).group("url")
            if link in message.text and 'dropmefiles.com' in message.text:
                await sql.execute(
                    f"UPDATE users SET cash = (cash - 50) WHERE id = '{message.from_user.id}'")
                await sql.execute(
                    f"INSERT INTO zaliv (linksender, zalivsender) VALUES ('{message.text}', '{message.from_user.id}')")
                await bot.send_message(message.from_user.id, "<b>Вы отправили заявку на залив! Ожидайте...</b>",
                                       parse_mode="html")
                await state.finish()
                await bot.send_message(ZALIV_CHAT_ID,
                                       '<b>🍪 Новая заявка на залив 🍪 </b>'
                                       '\n📹<b>Ссылка на архив:</b> {0}'
                                       '\n🔑 <b>Айди</b>: {1}'
                                       '\n👤<b>Имя:</b> {2}'
                                       '\n👤<b>Заказчик:</b> @{3}'.format(
                                           message.text, message.from_user.id, message.from_user.first_name,
                                           message.from_user.username), reply_markup=kb_zaliv_status,
                                       parse_mode="html")
                await sql.close()
        else:
            await message.answer('<b>Недостаточно средств! Пополните баланс.</b>', parse_mode="html")
            await state.finish()
            await sql.close()
    except(Exception,):
        await message.answer('<b>Загрузите архив на файлообменник dropmefiles</b>', parse_mode="html")
        await state.finish()
        await sql.close()
