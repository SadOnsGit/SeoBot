import re
import asyncpg
from auth_data import HOST, USER, PASSWORD, DB_NAME, ADMINS
from bot_create import dp, bot
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards.kb_status_seo import kb_status
from auth_data import SEO_CHAT_ID, QUEUEINFO_CHAT_ID


class Sendlinkyoutube(StatesGroup):
    step1 = State()


@dp.message_handler(state=Sendlinkyoutube.step1)
async def seoboost_create_exp(message: types.Message, state: FSMContext):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    usercash = await sql.fetch(f"SELECT cash FROM users WHERE id = {message.from_user.id}")
    queueinfo = await sql.fetch("SELECT queueID from queue")
    if usercash[0][0] < 150:
        await message.answer('<b>Недостаточно средств для отправления заявки! Пополните баланс!</b>',
                             parse_mode="html")
        await state.finish()
        return
    if queueinfo[0][0] == 5:
        await message.answer('<b>К сожалению, сейчас нет свободных мест на SEO, повторите попытку позже!</b>',
                             parse_mode="html")
        await state.finish()
        return
    try:
        link = re.search(r"(?P<url>https?://\S+)", message.text).group("url")
        if str(link) == str(message.text):
            if usercash[0][0] >= 150 and queueinfo[0][0] < 5:
                await seoboostsend(message)
                await state.finish()
        else:
            await message.answer('<b>Ошибка: укажите ссылку без лишних символов</b>', parse_mode="html")
            await state.finish()
    except(Exception,):
        await message.answer("<b>Это не то, что мне нужно, отправьте ссылку на ютуб видео!</b>",
                             parse_mode="html")
        await state.finish()
        await sql.close()


async def seoboostsend(message: types.Message):
    try:
        sql = await asyncpg.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DB_NAME
        )
        await sql.execute(
            f"INSERT INTO links (linkyoutube, linkid, linksender) VALUES "
            f"('{message.text}', NEXTVAL('links_linkid_seq'), '{message.from_user.id}')")
        await sql.execute(f"UPDATE users SET cash = (cash - 150) WHERE id = {message.from_user.id}")
        await sql.execute("UPDATE queue SET queueID = (queueID + 1)")
        await message.answer(
            '<b>Вы отправили заявку на накрутку SEO. С вашего баланса будет списано 150 рублей.</b>',
            parse_mode="html")
        queueinfo = await sql.fetch("SELECT queueID from queue")
        linkid = await sql.fetch(f"SELECT linkID FROM links WHERE linkYoutube = '{message.text}'")
        await sql.execute("UPDATE stats SET all_requests = (all_requests + 1)")
        await bot.send_message(SEO_CHAT_ID,
                               '<b>➡ Новая заявка на SEO №{0} 📈 </b>'
                               '\n📹Ссылка на видео: {1}\n🔑 Айди: {2}\n👤Имя: {3}\n👤Заказчик: @{4}'.format(
                                   linkid[0][0], message.text, message.from_user.id,
                                   message.from_user.first_name,
                                   message.from_user.username), parse_mode="html", reply_markup=kb_status)
        await bot.send_message(QUEUEINFO_CHAT_ID,
                               f'<b>[⚙] Поступила заявка на SEO, в очереди {queueinfo[0][0]} человек(а). '
                               f'\nОсталось мест: {5 - queueinfo[0][0]} шт.</b>',
                               parse_mode="html")
        await sql.close()
    except Exception as error:
        await bot.send_message(int(ADMINS[0]), f'<b>В боте произошла ошибка! \nОписание: {error}</b>',
                               parse_mode="html")
