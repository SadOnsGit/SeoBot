from aiogram import types
from auth_data import ADMINS
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from keyboards.kb_adminpanel import kb_adminpanel, kb_cancel_state
from bot_create import Dispatcher
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


class CreatePromocode(StatesGroup):
    step1_promocode = State()
    step2_amount = State()
    step3_usecount = State()


async def create_promocode(message: types.Message):
    if message.text == '🎁 Создать промокод' and message.from_user.id == int(ADMINS[0]):
        await message.answer('Введите промокод', reply_markup=kb_cancel_state)
        await CreatePromocode.step1_promocode.set()


async def promocode_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['promo'] = message.text
    await message.reply('Теперь введи сумму промокода', reply_markup=kb_cancel_state)
    await CreatePromocode.next()


async def promocode_amount(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['amount'] = message.text
    await message.reply('Теперь введи количество использований', reply_markup=kb_cancel_state)
    await CreatePromocode.next()


async def promocode_usecount(message: types.Message, state: FSMContext):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    async with state.proxy() as data:
        data['useCount'] = message.text
    async with state.proxy() as data:
        await sql.execute(
            f"""INSERT INTO promocodes (promocode, amount, usecount) 
            VALUES ('{data.get('promo')}', '{data.get('amount')}', '{data.get('useCount')}')""")
        await message.answer(f'<b>🎁 Вы успешно создали промокод = {data.get("promo")}'
                             f'\n🎁 Сумма промокода: {data.get("amount")} рублей'
                             f'\n🎁 Количество использований: {data.get("useCount")} раз</b>',
                             reply_markup=kb_adminpanel,
                             parse_mode="html")
    await state.finish()


async def cancel_create_promocode(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('<b>Действие отменено.</b>', parse_mode="html", reply_markup=kb_adminpanel)


def register_handlers_promocode(dp: Dispatcher):
    dp.register_message_handler(create_promocode, Text('🎁 Создать промокод'), state=None)
    dp.register_message_handler(cancel_create_promocode, Text('❌ Отмена'), state='*')
    dp.register_message_handler(promocode_text, state=CreatePromocode.step1_promocode)
    dp.register_message_handler(promocode_amount, state=CreatePromocode.step2_amount)
    dp.register_message_handler(promocode_usecount, state=CreatePromocode.step3_usecount)
