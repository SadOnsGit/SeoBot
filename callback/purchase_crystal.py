from aiogram import types
from bot_create import bot, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards.kb_purchase_method import kb_purchase_crystal_count
from external.pycrystalpay import CrystalPay
from auth_data import CRYSTAL_NAME, CRYSTAL_SECRET1, HOST, USER, PASSWORD, DB_NAME
import asyncpg

crystal = CrystalPay(CRYSTAL_NAME, CRYSTAL_SECRET1)


async def purchase_crystal(call: types.CallbackQuery):
    if call.data == 'purchase.crystal':
        await bot.send_message(call.message.chat.id,
                               "Вы выбрали платёжную систему <b>💎 CrystalPay</b>\n<b>Выберите сумму пополнения:</b>",
                               parse_mode="html", reply_markup=kb_purchase_crystal_count)


async def purchase_crystal_count(call: types.CallbackQuery):
    if call.data == 'crystalcount.150':
        await purchase_crystal_amount(150, call.message.chat.id, call.message.message_id)
        await call.answer()
    elif call.data == 'crystalcount.300':
        await purchase_crystal_amount(300, call.message.chat.id, call.message.message_id)
        await call.answer()
    elif call.data == 'crystalcount.600':
        await purchase_crystal_amount(600, call.message.chat.id, call.message.message_id)
        await call.answer('После оплаты, нажмите кнопку "Проверить оплату"', show_alert=True)


async def purchase_crystal_amount(amount, chat_id, message_id):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    pay_link = crystal.generate_pay_link(amount)
    markup_purchase = types.InlineKeyboardMarkup()
    purchase = types.InlineKeyboardButton(text='Оплатить', url=pay_link[1])
    check_purchase = types.InlineKeyboardButton(text='Проверить оплату', callback_data='check.purchase')
    markup_purchase.add(purchase, check_purchase)
    await sql.execute(f"UPDATE users SET pay_id = '{pay_link[0]}' WHERE id = '{chat_id}'")
    await bot.edit_message_text(chat_id=chat_id, message_id=message_id,
                                text=f"<b>Информация о платеже: \n"
                                     f"\nПлатежная система: 💎 CrystalPay "
                                     f"\nСумма платежа: {amount} рублей</b>",
                                parse_mode="html",
                                reply_markup=markup_purchase)


async def check_purchase_crystal(call: types.CallbackQuery):
    sql = await asyncpg.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DB_NAME
    )
    if call.data == 'check.purchase':
        payid = await sql.fetch(f"SELECT pay_id FROM users WHERE id = '{call.message.chat.id}'")
        datapayment = crystal.get_pay_status(payid[0][0])
        if datapayment[0] is True:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                        text=f"<b> Вы успешно пополнили баланс на {datapayment[1]} "
                                             f"рублей!✅</b>",
                                        parse_mode="html")
            await sql.execute(
                f"UPDATE users SET cash = (cash + {datapayment[1]}) WHERE id = '{call.message.chat.id}'")
        else:
            await bot.send_message(call.message.chat.id, "<b>❌ Платёж не был найден!</b>", parse_mode="html")


def register_callback_crystal(dp: Dispatcher):
    dp.register_callback_query_handler(purchase_crystal, Text(startswith='purchase.'))
    dp.register_callback_query_handler(purchase_crystal_count, Text(startswith='crystalcount.'))
    dp.register_callback_query_handler(check_purchase_crystal, Text(startswith='check.'))
