import logging
from configs import settings

from auth import authorization
from commands import get_cost, trand, get_cookie
from commands import average15, average50, get_dividents
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from client_info import client_info

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text('Добро пожаловать в телеграм бот предоставляющий информацию с Московской биржи moex.ru ')


def main():
    authorization.get_auth()  # авторизация на бирже по логину и паролю. Получение токена для дальнейшего использования.
    print(authorization.get_auth())
    mybot = Updater(settings.BOT_API_KEY,
                    use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("div", get_dividents.get_dividents_info))
    dp.add_handler(CommandHandler("trand", trand.get_trand_status))
    dp.add_handler(CommandHandler("price", get_cost.get_cost))
    dp.add_handler(CommandHandler("average15", average15.get_15_days_average))
    dp.add_handler(CommandHandler("average50", average50.get_50_days_average))
    dp.add_handler(CommandHandler('cookie', get_cookie.getcookie))  # Временная функция для внутренней проверки куки.
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(MessageHandler(Filters.text, client_info))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
