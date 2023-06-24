from bot_create import bot
from aiogram import types
from keyboards.kb_purchase_method import kb_purchase_method


async def pre_purchase(message: types.Message):
    await bot.send_message(message.from_user.id, "<b>💸 Выберите способ пополнения</b>", parse_mode="html",
                     reply_markup=kb_purchase_method)