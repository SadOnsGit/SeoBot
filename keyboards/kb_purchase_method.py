from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

kb_purchase_method = InlineKeyboardMarkup()
kb_purchase_crystal = InlineKeyboardButton(text='💎 CrystalPay', callback_data='purchase.crystal')
kb_use_promocode = InlineKeyboardButton(text='🎁 Использовать промокод', callback_data='use.promocode')

kb_purchase_method.add(kb_purchase_crystal).add(kb_use_promocode)

kb_purchase_crystal_count = InlineKeyboardMarkup()
kb_purchase_crystal_count_150 = InlineKeyboardButton(text='150', callback_data='crystalcount.150')
kb_purchase_crystal_count_300 = InlineKeyboardButton(text='300', callback_data='crystalcount.300')
kb_purchase_crystal_count_600 = InlineKeyboardButton(text='600', callback_data='crystalcount.600')

kb_purchase_crystal_count.add(kb_purchase_crystal_count_150, kb_purchase_crystal_count_300,
                              kb_purchase_crystal_count_600)
