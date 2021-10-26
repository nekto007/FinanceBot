from api.moex.price import (
    get_all_tickers
)
from clients.client_info import post_client_info
from cron.crons import (
    create_cron,
    list_cron,
    remove_cron,
)


def notification(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    chat_id = update.message.chat.id
    if len(text) == 1:
        update.message.reply_text('Введите тикер на обновление которого вы хотите подписаться\n')
    elif len(text) == 3 and text[1] == 'remove':
        ticket = text[2].upper()
        remove_status = remove_cron(ticket, chat_id, 'notification')
        if remove_status:
            update.message.reply_text(f'Вы удалили подписку на {ticket}.')
        else:
            update.message.reply_text(f'У вас нет подписок по тикеру: {ticket}.')
    else:
        ticket = text[1].upper()
        tickers_list = get_all_tickers(emitet=ticket)
        if tickers_list:
            create_status = create_cron(ticket, chat_id, 'notification')
            if create_status:
                update.message.reply_text(f'<b>Вы успешно подписались на получение обновлений по тикету: {ticket}.\n'
                                          f'Каждый рабочий день в 09:00(мск) я отправлю тебе сообщение.</b>',
                                          parse_mode='HTML')
        else:
            update.message.reply_text(
                f'По {ticket} мы не смогли найти тикер.\n'
                f' Попробуйте изменить название тикера и сделать запрос повторно.')


def get_notifications(update, context):
    ticker_list = []
    chat_id = update.message.chat.id
    ticker_notification_list = list_cron(chat_id, 'notification')
    if ticker_notification_list:
        for ticker in ticker_notification_list:
            ticker_list.append(ticker[0])
        update.message.reply_text(f'Список тикеров на обновления которых вы подписаны: {", ".join(ticker_list)} \n')
    else:
        update.message.reply_text(f'<b>На данный момент у вас нет подписок на акции.</b>',
                                  parse_mode='HTML')


if __name__ == '__main__':
    pass
