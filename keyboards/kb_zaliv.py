from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

kb_zaliv_access = InlineKeyboardMarkup()
btn_zaliv_access = InlineKeyboardButton('🍪 Отправить заявку', callback_data='zaliv.access')


kb_zaliv_access.add(btn_zaliv_access)

kb_zaliv_status = InlineKeyboardMarkup()
btn_zaliv_status_yes = InlineKeyboardButton('Успешно', callback_data='success.zaliv')
btn_zaliv_status_no = InlineKeyboardButton('Не успешно', callback_data='success.zalivno')

kb_zaliv_status.add(btn_zaliv_status_yes, btn_zaliv_status_no)
