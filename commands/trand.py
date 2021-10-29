import datetime

from api.moex.price import get_average
from clients.client_info import post_client_info


def get_trand_status(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        tickets = text[1:6]
        for ticket in tickets:
            average_15 = get_average(ticket.upper(), 15)
            if average_15 is not None:
                average_50 = get_average(ticket.upper(), 50)
                if average_15["average"] < average_50["average"]:
                    trand_course = 'Тренд идет вниз'
                else:
                    trand_course = 'Тренд идет вверх'
                update.message.reply_text(
                    f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
                    f'Наименование компании: {average_15["company_name"]} \n'
                    f'Наименование тикета: {average_15["ticket_name"]} \n'
                    f'Значение скользящей за 15 дней: {average_15["average"]} \n'
                    f'Значение скользящей за 50 дней: {average_50["average"]} \n'
                    f'Тренд стоимости акции: {trand_course}</b>'
                    , parse_mode='HTML')
            else:
                update.message.reply_text(f'По запросу {ticket} ничего не найдено. Попробуйте изменить название '
                                          f'акции и повторно сделать запрос.')


if __name__ == '__main__':
    pass
