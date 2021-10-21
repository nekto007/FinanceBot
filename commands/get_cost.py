import datetime
from api.moex.price import get_price
import os


def get_cost(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        tickets = text[1:]
        for ticket in tickets:
            price = get_price(ticket.upper())
            if price is not None:
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {price["company_name"]}\n'
                    f'Наименование тикета: {price["ticket_name"]} \n'
                    f'Стоимость акции: {(price["current_cost"])} \n'
                    f'Цена открытия: {price["open_price"]} \n'
                    f'Цена закрытия: {price["close_price"]} \n'
                    f'Минимальная стоимость за торги: {price["low_cost_daily"]} \n'
                    f'Максимальная стоимость за торги: {price["high_cost_daily"]} </b>\n'
                    , parse_mode='HTML')
                if price['graph_photo'] is not None:
                    update.message.reply_photo(open(price['graph_photo'], 'rb'))
                    os.remove(price['graph_photo'])
            else:
                update.message.reply_text(f'По запросу: {ticket} ничего не найдено. Попробуйте изменить '
                                          f'название акции и '
                                          'повторно сделать запрос.')


if __name__ == '__main__':
    pass
