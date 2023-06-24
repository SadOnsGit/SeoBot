from aiogram import types
from aiogram.dispatcher.filters import Text
from bot_create import bot, Dispatcher
from aiogram.dispatcher.filters.state import StatesGroup, State
import re
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


class Zaliv(StatesGroup):
    link = State()
    accept = State()


async def zaliv_send(call: types.CallbackQuery):
    if call.data == 'zaliv.access':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='<b>Отправьте ссылку на скачивание архива:</b>', parse_mode="html")
        await Zaliv.link.set()


async def status_zaliv(call: types.CallbackQuery):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    if call.data == 'success.zaliv':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{call.message.text}\n➖➖➖➖➖➖➖➖➖➖➖➖➖'
                                         f'\nУспешно выполнено ✅\n'
                                         f'Вышлите заказчику ссылку на видео в Личное сообщение')
        link = re.search(r"(?P<url>https?://\S+)", call.message.text).group("url")
        object_userid = await sql.fetch(f"SELECT zalivSender FROM zaliv WHERE linkSender='{link}'")
        await bot.send_message(object_userid[0][0], '<b>Ваша заявка на залив была выполнена успешно ✅'
                                                    '\nАдминистратор вышлет вам ссылку на видео '
                                                    'в личное сообщение!</b>',
                               parse_mode="html")
        await sql.execute(f"DELETE FROM zaliv WHERE linkSender = '{link}'")
        await sql.close()
    if call.data == 'success.zalivno':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text=f'{call.message.text}\n➖➖➖➖➖➖➖➖➖➖➖➖➖'
                                         f'\nФрод / Не успешно ❌')
        link = re.search(r"(?P<url>https?://\S+)", call.message.text).group("url")
        object_userid = await sql.fetch(f"SELECT zalivSender FROM zaliv WHERE linkSender='{link}'")
        await bot.send_message(object_userid[0][0], '<b>Ваша заявка на залив была отклонена ❌'
                                                    '\nДеньги были возвращены на баланс</b>',
                               parse_mode="html")
        await sql.execute(f"UPDATE users SET cash = (cash + 50) WHERE id = '{object_userid[0][0]}'")
        await sql.execute(f"DELETE FROM zaliv WHERE linkSender = '{link}'")
        await sql.close()


def register_callback_zaliv(dp: Dispatcher):
    dp.register_callback_query_handler(zaliv_send, Text(startswith='zaliv.'))
    dp.register_callback_query_handler(status_zaliv, Text(startswith='success.'))
