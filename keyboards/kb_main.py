from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_main = ReplyKeyboardMarkup(resize_keyboard=True)
btn_info = KeyboardButton('📱Профиль')
btn_seoboost = KeyboardButton('📈 Накрутка SEO')
btn_purchase = KeyboardButton('💵 Пополнить баланс')
btn_support = KeyboardButton('❓ Техническая поддержка')
btn_zaliv = KeyboardButton('🍪 Залив по кукам')
queue_info = KeyboardButton('🍃 Информация')
btn_send_all = KeyboardButton('Рассылка')

kb_main.row(btn_info, btn_seoboost)
kb_main.row(btn_purchase, btn_support)
kb_main.row(btn_zaliv, queue_info)
