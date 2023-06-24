from bot_create import bot, Dispatcher
from aiogram import types
from aiogram.dispatcher.filters import Text
from keyboards.kb_status_seo import kb_status_seo
from auth_data import QUEUEINFO_CHAT_ID
import re
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME, ADMINS


async def callback_inline(call: types.CallbackQuery):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    if call.data == 'callback.yes':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{call.message.text}\n➖➖➖➖➖➖➖➖➖➖➖➖➖'
                                         f'\nСтатус: Принято 🟢'
                                         f'\nЗаявку принял: @{call.from_user.username}',
                                    reply_markup=kb_status_seo)
        link = re.search(r"(?P<url>https?://\S+)", call.message.text).group("url")
        link_id = await sql.fetch(f"SELECT linkSender FROM links WHERE linkYoutube = '{link}'")
        await bot.send_message(link_id[0][0],
                               '<b>Ваша заявка на SEO была принята!</b>', parse_mode="html")
    elif call.data == 'callback.no':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{call.message.text}\n➖➖➖➖➖➖➖➖➖➖➖➖➖'
                                         f'\nСтатус: Отказано 🔴'
                                         f'\nЗаявку отказал: @{call.from_user.username}')
        link = re.search(r"(?P<url>https?://\S+)", call.message.text).group("url")
        link_id = await sql.fetch(f"SELECT linkSender FROM links WHERE linkYoutube = '{link}'")
        await sql.execute(f"UPDATE users SET cash = (cash + 150) WHERE id = '{link_id[0][0]}'")
        await sql.execute('UPDATE queue SET queueID = (queueID - 1)')
        await sql.execute(f"""DELETE FROM links WHERE linkYoutube = '{link}'""")
        await sql.execute("UPDATE stats SET cancel_requests = (cancel_requests + 1)")
        queueinfo = await sql.fetch("SELECT queueID from queue")
        await bot.send_message(link_id[0][0],
                               '<b>Ваша заявка на SEO была отклонена! Деньги возвращены на баланс</b>',
                               parse_mode="html")
        await bot.send_message(QUEUEINFO_CHAT_ID,
                               f'<b>[😋] Сейчас в очереди: {queueinfo[0][0]} человек(а),'
                               f' скорее закидывай на SEO! '
                               f'\nОсталось мест: {5 - queueinfo[0][0]} шт.</b>',
                               parse_mode="html")
        await sql.close()


async def callback_status_seo(call: types.CallbackQuery):
    try:
        sql = await asyncpg.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        if call.data == 'status.yes':
            link = re.search(r"(?P<url>https?://\S+)", call.message.text).group("url")
            link_id = await sql.fetch(f"SELECT linkSender FROM links WHERE linkYoutube = '{link}'")
            await bot.send_message(link_id[0][0],
                                   '<b>Ваша заявка на SEO была выполнена успешно!\nПожалуйста, оставьте отзыв</b>',
                                   parse_mode='html')
            await sql.execute(f"""DELETE FROM links WHERE linkYoutube = '{link}'""")
            await sql.execute('UPDATE queue SET queueID = (queueID - 1)')
            queueinfo = await sql.fetch("SELECT queueID from queue")
            await sql.execute("UPDATE stats SET success_requests = (success_requests + 1)")
            await sql.execute("UPDATE stats SET amount_earned = (amount_earned + 150)")
            await bot.send_message(QUEUEINFO_CHAT_ID,
                                   f'<b>[😋] Сейчас в очереди: {queueinfo[0][0]} '
                                   f'человек(а), скорее закидывай на SEO! '
                                   f'\nОсталось мест: {5 - queueinfo[0][0]} шт.</b>',
                                   parse_mode="html")
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{call.message.text}\n➖➖➖➖➖➖➖➖➖➖➖➖➖'
                                             f'\nУспешно выполнено ✅  ')
        if call.data == 'status.no':
            link = re.search(r"(?P<url>https?://\S+)", call.message.text).group("url")
            link_id = await sql.fetch(f"SELECT linkSender FROM links WHERE linkYoutube = '{link}'")
            await sql.execute(f"UPDATE users SET cash = (cash + 150) WHERE id = '{link_id[0][0]}'")
            await sql.execute(f"""DELETE FROM links WHERE linkYoutube = '{link}'""")
            await sql.execute('UPDATE queue SET queueID = (queueID - 1)')
            await sql.execute("UPDATE stats SET cancel_requests = (cancel_requests + 1)")
            queueinfo = await sql.fetch("SELECT queueID from queue")
            await bot.send_message(link_id[0][0],
                                   '<b>Ваша заявка на SEO была отклонена! Деньги возвращены на баланс</b>',
                                   parse_mode="html")
            await bot.send_message(QUEUEINFO_CHAT_ID,
                                   f'<b>[😋] Сейчас в очереди: {queueinfo[0][0]} человек(а),'
                                   f' скорее закидывай на SEO! '
                                   f'\nОсталось мест: {5 - queueinfo[0][0]} шт.</b>',
                                   parse_mode="html")
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f'{call.message.text}\n➖➖➖➖➖➖➖➖➖➖➖➖➖'
                                             f'\nНе выполнено ❌')
    except Exception as error:
        await bot.send_message(int(ADMINS[0]), f'<b>В боте произошла ошибка! \nОписание: {error}</b>',
                               parse_mode="html")


def register_callback_status_seo(dp: Dispatcher):
    dp.register_callback_query_handler(callback_inline, Text(startswith='callback.'))
    dp.register_callback_query_handler(callback_status_seo, Text(startswith='status.'))
