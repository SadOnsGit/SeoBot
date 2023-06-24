from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_cancel_send = InlineKeyboardMarkup()
btn_cancel_send = InlineKeyboardButton('Отменить 🔴', callback_data='cancelsend.seo')

kb_cancel_send.add(btn_cancel_send)
