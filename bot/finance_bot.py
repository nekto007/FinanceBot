import logging
import settings
from Price import get_price, get_average
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='finance_bot.log')


def greet_user(update, context):
    text = 'Вызван /start'
    update.message.reply_text('Добро пожаловать в телеграм бот предоставляющий информацию с Московской биржи moex.ru, '
                              'На данный момент я умею только /price')


def cost(update, context):
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


def average15(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().capitalize()
        average = get_average(ticket, 15)
        if average is not None:
            update.message.reply_text(
                f'Наименование компании: {average["company_name"]} \n'
                f'Наименование тикета: {average["ticket_name"]} \n'
                f'Значение скользящей за 15 дней: {average["average"]}')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')


def average50(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().capitalize()
        average = get_average(ticket, 50)
        if average is not None:
            update.message.reply_text(
                f'Наименование компании: {average["company_name"]} \n'
                f'Наименование тикета: {average["ticket_name"]} \n'
                f'Значение скользящей за 50 дней: {average["average"]}')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')


def trand(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().capitalize()
        average_15 = get_average(ticket, 15)
        if average15 is not None:
            average_50 = get_average(ticket, 50)
            if average_15["average"] < average_50["average"]:
                trand_course = 'Тренд идет вниз'
            else:
                trand_course = 'Тренд идет вверх'
            update.message.reply_text(
                f'Наименование компании: {average_15["company_name"]} \n'
                f'Наименование тикета: {average_15["ticket_name"]} \n'
                f'Значение скользящей за 15 дней: {average_15["average"]} \n'
                f'Значение скользящей за 50 дней: {average_50["average"]} \n'
                f'Тренд стоимости акции: {trand_course}')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')


def main():
    mybot = Updater(settings.BOT_API_KEY,
                    use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("trand", trand))
    dp.add_handler(CommandHandler("price", cost))
    dp.add_handler(CommandHandler("average15", average15))
    dp.add_handler(CommandHandler("average50", average50))
    dp.add_handler(CommandHandler("start", greet_user))

    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
