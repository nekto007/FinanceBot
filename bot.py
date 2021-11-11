import logging
from telegram.ext import (
    CommandHandler,
    Filters,
    MessageHandler,
    Updater
)

from auth import authorization
from bot import helper
from clients.client_info import post_client_info
from commands import (
    alerts,
    get_average,
    get_cookie,
    get_cost,
    get_dividents,
    get_tickers,
    notifications,
    trand,
)
from api.moex import currency
from configs import settings

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text('Добро пожаловать в телеграм бот предоставляющий информацию с Московской биржи moex.ru ')


def main():
    authorization.get_auth()  # авторизация на бирже по логину и паролю. Получение токена для дальнейшего использования.
    mybot = Updater(settings.BOT_API_KEY,
                    use_context=True)
    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("div", get_dividents.get_dividents_info))
    dp.add_handler(CommandHandler("trand", trand.get_trand_status))
    dp.add_handler(CommandHandler("price", get_cost.get_cost))
    dp.add_handler(CommandHandler("avg15", get_average.get_days_average))
    dp.add_handler(CommandHandler("avg50", get_average.get_days_average))
    dp.add_handler(CommandHandler('cookie', get_cookie.getcookie))  # Временная функция для внутренней проверки куки.
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("info", get_tickers.get_list_tickers))
    dp.add_handler(CommandHandler("alert", alerts.alerts))
    dp.add_handler(CommandHandler("list_alert", alerts.get_alerts))
    dp.add_handler(CommandHandler("subs", notifications.notification))
    dp.add_handler(CommandHandler("list_subs", notifications.get_notifications))
    dp.add_handler(CommandHandler("curr", currency.get_all_currency))
    dp.add_handler(CommandHandler("hist", currency.get_hist_curr))
    dp.add_handler(CommandHandler("rub", currency.rub))
    dp.add_handler(CommandHandler("usd", currency.usd))
    dp.add_handler(CommandHandler("eur", currency.eur))
    dp.add_handler(CommandHandler("help", helper.help))
    dp.add_handler(MessageHandler(Filters.text, post_client_info))
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
