from menu.profile import profile
from menu.seoboost import seoboost
from menu.purchase_method import pre_purchase
from bot_create import Dispatcher
from menu.support import support
from menu.zaliv import zaliv
from menu.queue_info import infoqueue


async def main(message):  # Определяем тип инцидента и уточняем его подтип
    if message.text == '📱Профиль':
        await profile(message)
    elif message.text == '📈 Накрутка SEO':
        await seoboost(message)
    elif message.text == '💵 Пополнить баланс':
        await pre_purchase(message)
    elif message.text == '❓ Техническая поддержка':
        await support(message)
    elif message.text == '🍪 Залив по кукам':
        await zaliv(message)
    elif message.text == '🍃 Информация':
        await infoqueue(message)
    else:
        pass


def register_handler_menu(dp: Dispatcher):
    dp.register_message_handler(main)
