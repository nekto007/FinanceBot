import datetime
import os

from api.moex.price import get_average
from clients.client_info import post_client_info
from get_candles import get_graph


def get_trand_status(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        tickets = text[1:6]
        for ticket in tickets:
            history_price_15 = get_average(ticket.upper(), 15)
            if history_price_15 is not None:
                average_15 = round(sum(history_price_15[0]) / len(history_price_15[0]), 3)
                short_name = history_price_15[1]
                history_price_50 = get_average(ticket.upper(), 50)
                average_50 = round(sum(history_price_50[0]) / len(history_price_50[0]), 3)
                if average_15 < average_50:
                    trand_course = 'Тренд идет вниз'
                else:
                    trand_course = 'Тренд идет вверх'
                graph_photo = get_graph(ticket.upper(), 50)
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {short_name} \n'
                    f'Наименование тикета: {ticket.upper()} \n'
                    f'Значение скользящей за 15 дней: {average_15} \n'
                    f'Значение скользящей за 50 дней: {average_50} \n'
                    f'Тренд стоимости акции: {trand_course}</b>'
                    , parse_mode='HTML')
                if graph_photo is not None:
                    with open(graph_photo, 'rb') as photo:
                        update.message.reply_photo(photo)
                        os.remove(graph_photo)
            else:
                update.message.reply_text(f'По запросу {ticket} ничего не найдено. Попробуйте изменить название '
                                          f'акции и повторно сделать запрос.')


if __name__ == '__main__':
    pass
