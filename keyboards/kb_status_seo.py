from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_status = InlineKeyboardMarkup()
kb_status_yes = InlineKeyboardButton(text='Принять', callback_data='callback.yes')
kb_status_no = InlineKeyboardButton(text='Отказаться', callback_data='callback.no')

kb_status.add(kb_status_yes, kb_status_no)

kb_status_seo = InlineKeyboardMarkup()
kb_status_yes = InlineKeyboardButton(text='Успешно', callback_data='status.yes')
kb_status_no = InlineKeyboardButton(text='Не успешно', callback_data='status.no')

kb_status_seo.add(kb_status_yes, kb_status_no)
