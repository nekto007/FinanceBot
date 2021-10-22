import datetime
import os

from api.moex.price import get_average


def get_days_average(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        tickets = text[1:]
        days = text[0][-2:]
        for ticket in tickets:
            average = get_average(ticket.upper(), int(days))
            print('average', average)
            if average is not None:
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {average["company_name"]} \n'
                    f'Наименование тикета: {average["ticket_name"]} \n'
                    f'Значение скользящей за 15 дней: {average["average"]}</b>'
                    , parse_mode='HTML')
                if average['candle_photo'] is not None:
                    with open(average['candle_photo'], 'rb') as candle_photo:
                        update.message.reply_photo(candle_photo)
                        os.remove(average['candle_photo'])
            else:
                update.message.reply_text(f'По запросу: {ticket} ничего не найдено. '
                                          f'Попробуйте изменить название акции и '
                                          'повторно сделать запрос.')


if __name__ == '__main__':
    pass
