from bot_create import bot
from aiogram import types


async def support(message: types.Message):
    await bot.send_message(message.from_user.id, '<b>Техническая поддержка: @godseo_support </b>', parse_mode="html")
