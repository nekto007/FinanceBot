import datetime
import os

from api.moex.price import get_average
from clients.client_info import post_client_info
from get_candles import get_candle


def get_days_average(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        tickets = text[1:6]
        days = int(text[0][-2:])
        for ticket in tickets:
            history_price = get_average(ticket.upper(), days)
            print('history_price', history_price)
            if history_price is not None:
                candle_photo = get_candle(ticket.upper(), days)
                average = round(sum(history_price[0]) / len(history_price[0]), 3)
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {history_price[1]} \n'
                    f'Наименование тикета: {ticket} \n'
                    f'Значение скользящей за {days} дней: {"₽{:,.2f}".format(average)}</b>', parse_mode='HTML')
                if candle_photo is not None:
                    with open(candle_photo, 'rb') as photo:
                        update.message.reply_photo(photo)
                        os.remove(candle_photo)
            else:
                update.message.reply_text(f'По запросу: {ticket} ничего не найдено. '
                                          f'Попробуйте изменить название акции и '
                                          'повторно сделать запрос.')


if __name__ == '__main__':
    pass
