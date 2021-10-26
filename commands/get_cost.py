import datetime
import os

from api.moex.price import get_price
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
                if price["close_price"]:
                    close_price = f'Цена закрытия: {price["close_price"]} \n'
                else:
                    close_price = f''
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {price["company_name"]}\n'
                    f'Наименование тикета: {price["ticket_name"]} \n'
                    f'Стоимость акции: {(price["current_cost"])} \n'
                    f'Цена открытия: {price["open_price"]} \n'
                    f'{close_price}'
                    f'Минимальная стоимость за торги: {price["low_cost_daily"]} \n'
                    f'Максимальная стоимость за торги: {price["high_cost_daily"]} </b>\n'
                    , parse_mode='HTML')
                if price['graph_photo'] is not None:
                    with open(price['graph_photo'], 'rb') as graph_photo:
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
