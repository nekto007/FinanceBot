from api.moex.price import (
    get_all_tickers,
    get_price,
)
from clients.client_info import post_client_info
from cron.crons import (
    create_cron,
    list_cron,
    remove_cron,
)


def alerts(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    chat_id = update.message.chat.id
    if len(text) == 1 or len(text) != 3:
        update.message.reply_text(
            'Введите тикер и цену при которой надо прислать оповещение.\n '
            'Например: /alert SBER 354.12 — Добавить оповещение'
            '(SBER — тикер, 354.12 — цена, на которой придет уведомление)\n'
            '/alert remove SBER — Все оповещения по тикеру SBER будут удалены')
    elif len(text) == 3 and text[1] == 'remove':
        ticket = text[2].upper()
        remove_status = remove_cron(ticket, chat_id, 'alert')
        if remove_status:
            update.message.reply_text(f'Количество удаленных оповещений по тикеру {ticket}: {remove_status}.')
        else:
            update.message.reply_text(f'У вас нет настроенных оповещений по тикеру {ticket}.')
    else:
        ticket = text[1].upper()
        cost = text[2]
        tickers_list = get_all_tickers(emitet=ticket)
        current_cost = get_price(ticket)
        if current_cost == cost:
            update.message.reply_text(f'<b>Стоимость тикера уже равна цене указанной вами в оповещении.</b>',
                                      parse_mode='HTML')
        elif tickers_list:
            create_status = create_cron(ticket, chat_id, 'alert', cost=cost)
            if create_status:
                if current_cost['current_cost'] / 100 > float(cost):
                    update.message.reply_text(f'<b>Когда цена {tickers_list[0][1]}({ticket}) упадет до '
                                              f'{"{:,.2f}₽".format(cost / 100)}руб.'
                                              f', я отправлю тебе сообщение.</b>',
                                              parse_mode='HTML')
                else:
                    update.message.reply_text(f'<b>Когда цена {tickers_list[0][1]}({ticket}) вырастет до '
                                              f'{"{:,.2f}₽".format(cost / 100)}руб.'
                                              f', я отправлю тебе сообщение.</b>',
                                              parse_mode='HTML')
        else:
            update.message.reply_text(
                f'По запросу: {ticket} мы не смогли найти указанный тикер.'
                f' Попробуйте изменить название тикера и сделать запрос повторно.')


def get_alerts(update, context):
    chat_id = update.message.chat.id
    alerts_list = list_cron(chat_id, 'alert')
    if alerts_list:
        current_cost = get_price(alerts_list[0][0])
        update.message.reply_text(f'Список оповещений для: {alerts_list[0][0]} - '
                                  f'Текущая цена: {"{:,.2f}₽".format(current_cost["current_cost"] / 100)}\n')
        if current_cost['current_cost'] > int(alerts_list[0][1]):
            update.message.reply_text(f'Оповещение сработает когда цена вырастет до '
                                      f'{"{:,.2f}₽".format(alerts_list[0][1] / 100)}')
        else:
            update.message.reply_text(f'Оповещение сработает когда цена упадет до '
                                      f'{"{:,.2f}₽".format(alerts_list[0][1] / 100)}')
    else:
        update.message.reply_text(f'<b>На данный момент твой список оповещений пустой.</b>',
                                  parse_mode='HTML')


if __name__ == '__main__':
    pass
