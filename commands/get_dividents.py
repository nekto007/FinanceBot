from api.moex.price import get_date_dividents


def get_dividents_info(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().upper()
        dividents = get_date_dividents(ticket)
        if dividents is not None:
            update.message.reply_text(
                'Дата, до которой включительно необходимо купить акции биржевых эмитетов для получения дивидендов \n'
                'Дата \t\t\t\t\t\t\t\t\t\t\t Сумма'
            )
            for divident in sorted(dividents, reverse=True):
                update.message.reply_text(f'{divident[2]}\t\t{divident[3]} {divident[4]}')
        else:
            update.message.reply_text(f'По указанному тикеру {ticket} дивидендов не найдено. '
                                      f'Попробуйте изменить название акции и повторно сделать запрос.')


# if __name__ == '__main__':
#     pass
