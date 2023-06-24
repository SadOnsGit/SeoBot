from aiogram import types
from handlers.seoboostlink import Sendlinkyoutube
from keyboards.kb_send_seo import kb_cancel_send


async def seoboost(message: types.Message):
    await message.answer('<b>SEO Boost ❤ \nСтоимость услуги - 150 рублей ✔\n\nОтправьте ссылку на видео:</b>',
                         parse_mode="html", reply_markup=kb_cancel_send)
    await Sendlinkyoutube.step1.set()
