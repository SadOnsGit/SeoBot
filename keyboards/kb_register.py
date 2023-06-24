from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btn_yes = KeyboardButton('Да')
btn_no = KeyboardButton('Нет')

kb_reg = ReplyKeyboardMarkup(resize_keyboard=True)

kb_reg.add(btn_yes).add(btn_no)
