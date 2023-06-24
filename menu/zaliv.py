from bot_create import bot
from aiogram import types
from keyboards.kb_zaliv import kb_zaliv_access


async def zaliv(message: types.Message):
    await bot.send_message(message.from_user.id,
                           "<b>Перед отправлением заявки, убедитесь что в архиве присутствуют файлы:"
                           "\nВидео, описание, теги, превью, куки канала + UserInformation.txt\n"
                           "Если отсутствует один из файлов ваша заявка будет отклонена!\n"
                           "Если в логе несколько каналов, "
                           "внутри архива укажите на какой именно канал нужно залить!"
                           "\nСтоимость услуги: 50 рублей\nАрхив нужно заливать на http://dropmefiles.com</b>",
                           parse_mode="html",
                           reply_markup=kb_zaliv_access)
