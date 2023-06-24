from aiogram import types
from aiogram.dispatcher.filters import Text
from bot_create import bot, Dispatcher
from aiogram.dispatcher import FSMContext


async def cancel_seo_send(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'cancelsend.seo':
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                    text='<b>Действие отменено.</b>', parse_mode="html")
        await state.finish()


def register_cancel_btn(dp: Dispatcher):
    dp.register_callback_query_handler(cancel_seo_send, Text(startswith='cancelsend.'), state='*')
