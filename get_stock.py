import requests

def get_stock(update, context):
    ticket = update.message.text.split()[1]
    response = requests.get(f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{ticket}.json?iss.meta=off')
    moex_answer = response.json()
    moex_indexes = list(moex_answer['marketdata'].values())[0]
    moex_values = list(moex_answer['marketdata'].values())[1:]
    for x in moex_values[0]:
        update.message.reply_text(f'Наименование тикета: {x[0]}, Режим торговой сессии: {x[1]}, Цена открытия: {x[9]}, Цена закрытия: {x[23]}')

if __name__ == '__main__':
    get_stock()