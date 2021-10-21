from api.moex.price import get_average


def get_15_days_average(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().upper()
        average = get_average(ticket, 15)
        if average is not None:
            update.message.reply_text(
                f'Наименование компании: {average["company_name"]} \n'
                f'Наименование тикета: {average["ticket_name"]} \n'
                f'Значение скользящей за 15 дней: {average["average"]}')
            if average['candle_photo'] is not None:
                update.message.reply_photo(open(average['candle_photo'], 'rb'))
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')


if __name__ == '__main__':
    pass
