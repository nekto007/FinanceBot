from api.moex.price import get_all_tickers


def get_list_tickers(update, context):
    text = update.message.text.split()
    if len(text) == 2:
        ticker_info = get_all_tickers(emitet=text[1])
        if ticker_info is not None:
            update.message.reply_text(
                f'<b>Наименование компании: {ticker_info[1]}\n'
                f'Наименование тикета: {ticker_info[0]}\n'
                f'Наименование биржи: {(ticker_info[2])} </b>\n'
                , parse_mode='HTML')
        else:
            update.message.reply_text('По вашему запросу ничего не найдено. Попробуйте изменить название акции и '
                                      'повторно сделать запрос.')

    else:
        tickers_info = []
        tickers_data = get_all_tickers()
        for ticker in tickers_data:
            tickers_info.append(ticker[0])
        update.message.reply_text(
            f'<b>Список Акции торгующихся на бирже: </b>{tickers_info} \n'
            , parse_mode='HTML')
