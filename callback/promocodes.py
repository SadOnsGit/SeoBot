from aiogram import types
from bot_create import Dispatcher, bot
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


class Promocodes(StatesGroup):
    step1_input = State()


async def use_promocode(call: types.CallbackQuery):
    if call.data == 'use.promocode':
        await bot.send_message(call.message.chat.id, '<b>Введите промокод</b>', parse_mode="html")
        await Promocodes.step1_input.set()


async def promocode_input(message: types.Message, state: FSMContext):
    try:
        sql = await asyncpg.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        promocode = await sql.fetch(f"SELECT * FROM promocodes WHERE promocode = '{message.text}'")
        promocode_use_user = await sql.fetch(f'SELECT promocode FROM users WHERE id = {message.from_user.id}')
        if promocode[0][0] == message.text and message.text == str(promocode_use_user[0][0]):
            await message.answer(
                '<b> Вы уже использовали данный промокод!\nДайте воспользоваться другим! :)</b>',
                parse_mode="html")
            await state.finish()
            return
        if promocode[0][0] == message.text and promocode[0][2] >= 1:
            amount = await sql.fetch(f"SELECT amount FROM promocodes WHERE promocode = '{message.text}'")
            await sql.execute(f"UPDATE users SET cash = (cash + {amount[0][0]}) WHERE id = '{message.from_user.id}'")
            await sql.execute(f"UPDATE users SET promocode = '{message.text}' WHERE id = '{message.from_user.id}'")
            await sql.execute(f"UPDATE promocodes SET useCount = (useCount - 1) WHERE promocode = '{message.text}'")
            await message.answer(f'<b>Вы успешно использовали промокод {message.text}'
                                 f'\nНа ваш баланс было зачислено {amount[0][0]} рублей.</b>',
                                 parse_mode="html")
            await state.finish()
            await sql.close()
        else:
            await message.answer('<b>Данный промокод использовали макс.количество раз!</b>', parse_mode="html")
            await state.finish()
    except(Exception,):
        await message.answer('<b>Ошибка: такого промокода не существует!</b>', parse_mode="html")
        await state.finish()


def registration_function_promocodes(dp: Dispatcher):
    dp.register_callback_query_handler(use_promocode, Text(startswith='use.'))
    dp.register_message_handler(promocode_input, state=Promocodes.step1_input)
