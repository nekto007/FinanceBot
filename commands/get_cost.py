import datetime
import os

from api.moex.price import get_price
from get_candles import get_graph
from clients.client_info import post_client_info


def get_cost(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        tickets = text[1:6]
        for ticket in tickets:
            price = get_price(ticket.replace(',', '').upper())
            if price is not None and price != 'Нет сделок':
                if price[3] != '':
                    close_price = f'Цена закрытия: {"{:,.2f}₽".format(price[3] / 100)} \n'
                    graph_photo = get_graph(ticket.replace(',', '').upper(), 15)
                else:
                    close_price = f''
                    graph_photo = None
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {price[6]}\n'
                    f'Наименование тикета: {price[0]} \n'
                    f'Стоимость акции: {"{:,.2f}₽".format(price[1] / 100)} \n'
                    f'Цена открытия: {"{:,.2f}₽".format(price[2] / 100)} \n'
                    f'{close_price}'
                    f'Минимальная стоимость за торги: {"{:,.2f}₽".format(price[4] / 100)} \n'
                    f'Максимальная стоимость за торги: {"{:,.2f}₽".format(price[5] / 100)} </b>\n'
                    , parse_mode='HTML')
                if graph_photo is not None:
                    with open(graph_photo, 'rb') as graph_photo:
                        update.message.reply_photo(graph_photo)
                        os.remove(price['graph_photo'])
            elif price == 'Нет сделок':
                update.message.reply_text(
                    f'<b>По выбранному тикеру: {ticket} на данный момент не было сделок.</b>', parse_mode='HTML')
            else:
                update.message.reply_text(
                    f'<b>По запросу: {ticket} ничего не найдено.\n'
                    f'Попробуйте изменить название акции и повторно сделать запрос или сделать запрос завтра.</b>',
                    parse_mode='HTML')


if __name__ == '__main__':
    pass
