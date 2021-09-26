import logging
import settings
from Price import get_price
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='finance_bot.log')


def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text('Добро пожаловать в телеграм бот предоставляющий информацию с Московской биржи moex.ru, '
                              'На данный момент я умею только /price')


def get_cost(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().capitalize()
        price = get_price(ticket)
        if price is not None:
            update.message.reply_text(
                f'Наименование тикета: {price["ticket_name"]} \n'
                f'Стоимость акции: {price["cost"]} \n'
                f'Цена открытия: {price["cost_open"]} \n'
                f'Цена закрытия: {price["cost_close"]} \n'
                f'Максимальная стоимость за торги: {price["max_cost"]} \n'
                f'Минимальная стоимость за торги: {price["min_cost"]} \n')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')


def main():
    mybot = Updater(settings.BOT_API_KEY,
                    use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("price", get_cost))
    dp.add_handler(CommandHandler("start", greet_user))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
