from bot_create import bot, Dispatcher
from aiogram import types
from auth_data import ADMINS
from keyboards.kb_adminpanel import kb_adminpanel, kb_cancel_state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME


class SendAllAds(StatesGroup):
    step1_photo = State()
    step2_text = State()
    step3_btn_name1 = State()
    step4_btn_url1 = State()
    step5_btn_name2 = State()
    step6_btn_name2_url = State()


class SendAllMsg(StatesGroup):
    step1_text = State()


async def handler_admin_panel(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        await message.answer(f'<b>Добро пожаловать в админ-панель, {message.from_user.first_name}'
                             f'\nЧто бы выйти из админ-панели введи команду /start </b>', parse_mode="html",
                             reply_markup=kb_adminpanel)


async def handler_sendall_msgs(message: types.Message):
    if message.text == '📩 Сообщение для пользователей' and str(message.from_user.id) in ADMINS:
        await message.answer('<b>Введите сообщение (можно использовать html-теги)</b>', parse_mode="html")
        await SendAllMsg.step1_text.set()


async def handler_sendall_ads(message: types.Message):
    if message.text == '💲 Реклама' and str(message.from_user.id) in ADMINS:
        await message.answer('<b>Загрузите фото для рекламы'
                             '\nДля корректной работы рассылки обязательна фотография</b>', parse_mode='html',
                             reply_markup=kb_cancel_state)
        await SendAllAds.step1_photo.set()


async def sendall_message(message: types.Message, state: FSMContext):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    users = await sql.fetch("SELECT id FROM users")
    for row in users:
        try:
            await bot.send_message(row[0], message.text, parse_mode="html")
        except(Exception,):
            continue

    await message.answer('<b>Рассылка была выполнена успешно!</b>', parse_mode="html",
                         reply_markup=kb_adminpanel)
    await state.finish()
    await sql.close()


async def start_sending_all(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[0].file_id
    await SendAllAds.next()
    await message.reply('Теперь, введи текст для рассылки (можно использовать html-теги)', reply_markup=kb_cancel_state)


async def take_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['text'] = message.text
    await SendAllAds.next()
    await message.reply('Теперь введи название первой инлайн кнопки', reply_markup=kb_cancel_state)


async def take_name_btn1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_name1'] = message.text
    await SendAllAds.next()
    await message.reply('Теперь введи ссылку перехода при нажатии на первую инлайн кнопку',
                        reply_markup=kb_cancel_state)


async def take_url_btn1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_url1'] = message.text
    await SendAllAds.next()
    await message.reply('Теперь введи название второй кнопки', reply_markup=kb_cancel_state)


async def take_name_btn2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['btn_name2'] = message.text
    await SendAllAds.next()
    await message.reply('Теперь введи ссылку перехода при нажатии на вторую инлайн кнопку',
                        reply_markup=kb_cancel_state)


async def take_url_btn2(message: types.Message, state: FSMContext):
    try:
        sql = await asyncpg.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        async with state.proxy() as data:
            data['btn_url2'] = message.text
        users = await sql.fetch("SELECT id FROM users")
        async with state.proxy() as data:
            #   Создание кнопок для рассылки
            sendall_markup = InlineKeyboardMarkup()
            btn1_sendall = InlineKeyboardButton(data.get('btn_name1'), url=data.get('btn_url1'))
            btn2_sendall = InlineKeyboardButton(data.get('btn_name2'), url=data.get('btn_url2'))
            sendall_markup.add(btn1_sendall, btn2_sendall)
            for rows in users:
                try:
                    await bot.send_photo(rows[0], data.get('photo'), caption=data.get('text'),
                                         reply_markup=sendall_markup,
                                         parse_mode="html")
                except(Exception,):
                    continue
        await state.finish()
        await message.answer('<b>Рассылка была выполнена успешно!</b>', parse_mode="html",
                             reply_markup=kb_adminpanel)
        await sql.close()
    except Exception as error:
        bot.send_message(int(ADMINS[0]), f'<b>В боте произошла ошибка!\nОписание: {error}</b>', parse_mode="html")


async def cancel_sendads_or_msgs(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer('<b>Действие отменено.</b>', parse_mode="html", reply_markup=kb_adminpanel)


async def stats_seo(message: types.Message):
    if str(message.from_user.id) in ADMINS:
        sql = await asyncpg.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        requests_seo = await sql.fetch("SELECT all_requests FROM stats")
        access_req_seo = await sql.fetch("SELECT success_requests FROM stats")
        cancel_req_seo = await sql.fetch("SELECT cancel_requests FROM stats")
        amount_earned = await sql.fetch("SELECT amount_earned FROM stats")
        await message.answer(f'<b>Статистика по боту:\nВсего заявок: {requests_seo[0][0]} шт.'
                             f'\nИз них успешно выполненных: {access_req_seo[0][0]} шт.'
                             f'\nОтклонённых: {cancel_req_seo[0][0]} шт.'
                             f'\nВсего заработано: {amount_earned[0][0]} рублей.</b>',
                             parse_mode="html")
        await sql.close()


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(handler_admin_panel, commands=['admin'])
    dp.register_message_handler(handler_sendall_ads, Text('💲 Реклама'), state=None)
    dp.register_message_handler(handler_sendall_msgs, Text('📩 Сообщение для пользователей'), state=None)
    dp.register_message_handler(start_sending_all, content_types=['photo'], state=SendAllAds.step1_photo)
    dp.register_message_handler(take_text, state=SendAllAds.step2_text)
    dp.register_message_handler(take_name_btn1, state=SendAllAds.step3_btn_name1)
    dp.register_message_handler(take_url_btn1, state=SendAllAds.step4_btn_url1)
    dp.register_message_handler(take_name_btn2, state=SendAllAds.step5_btn_name2)
    dp.register_message_handler(take_url_btn2, state=SendAllAds.step6_btn_name2_url)
    dp.register_message_handler(sendall_message, state=SendAllMsg.step1_text)
    dp.register_message_handler(cancel_sendads_or_msgs, Text('❌ Отмена'), state='*')
    dp.register_message_handler(stats_seo, Text('📈 Cтатистика'))
