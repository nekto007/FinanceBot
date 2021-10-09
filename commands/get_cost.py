from api.moex.price import get_price


def get_cost(update, context):
    text = update.message.text.split()
    if len(text) == 1:
        update.message.reply_text("Введите ticket интересующуй вас акции")
    else:
        ticket = text[1].lower().capitalize()
        price = get_price(ticket)
        if price is not None:
            update.message.reply_text(
                f'Наименование тикета: {price["ticket_name"]} \n'
                f'Стоимость акции: {price["cost"]} \n'
                f'Цена открытия: {price["cost_open"]} \n'
                f'Цена закрытия: {price["cost_close"]} \n'
                f'Максимальная стоимость за торги: {price["max_cost"]} \n'
                f'Минимальная стоимость за торги: {price["min_cost"]} \n')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')

if __name__ == '__main__':
    pass