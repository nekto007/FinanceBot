from api.moex.price import get_price


def get_cost(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().upper()
        price = get_price(ticket)
        if price is not None:
            update.message.reply_text(
                f'Наименование тикета: {price[0]} \n'
                f'Стоимость акции: {(price[1])/100} \n'
                f'Цена открытия: {price[2]/100} \n'
                f'Цена закрытия: {price[3]/100} \n'
                f'Максимальная стоимость за торги: {price[4]/100} \n'
                f'Минимальная стоимость за торги: {price[5]/100} \n')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')


if __name__ == '__main__':
    pass