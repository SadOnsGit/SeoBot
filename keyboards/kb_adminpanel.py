from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_adminpanel = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btn_sendall_ad = KeyboardButton('💲 Реклама')
btn_sendall = KeyboardButton('📩 Сообщение для пользователей')
btn_create_promocode = KeyboardButton('🎁 Создать промокод')
btn_stats = KeyboardButton('📈 Cтатистика')

kb_adminpanel.add(btn_sendall_ad, btn_sendall, btn_create_promocode).add(btn_stats)

kb_cancel_state = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn_cancel_state = KeyboardButton('❌ Отмена')

kb_cancel_state.add(btn_cancel_state)
