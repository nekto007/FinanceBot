import datetime

import prettytable as pt
from telegram import ParseMode

from api.moex.price import get_date_dividents
from clients.client_info import post_client_info


def get_dividents_info(update, context):
    post_client_info(update, '')
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().upper()
        dividents = get_date_dividents(ticket)
        if dividents is not None:
            table = pt.PrettyTable(['Дата', 'Сумма'])
            table.align['Дата'] = 'c'
            table.align['Сумма'] = 'r'
            update.message.reply_text(
                f'Текущая дата: {datetime.datetime.now().date()}\n'
                f'Дата, до которой включительно необходимо купить акции биржевых эмитетов для получения дивидендов \n'
            )
            for divident in sorted(dividents, reverse=True):
                table.add_row([divident[2], f'{divident[3]} {divident[4]}'])
            update.message.reply_text(f'<pre>{table}</pre>',
                                      parse_mode=ParseMode.HTML)
        else:
            update.message.reply_text(f'По указанному тикеру {ticket} дивидендов не найдено. '
                                      f'Попробуйте изменить название акции и повторно сделать запрос.')
