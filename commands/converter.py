import requests

def rub(update, context):
    currency_info = {}
    text = update.message.text.split()
    value = float(text[1])
    url = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json?iss.meta=off'
    response = requests.get(url)
    currency_data = response.json()['securities']['data']
    for _x in currency_data:
        currency_info[_x[2]]=_x[3]
    return update.message.reply_text(f"USD : {round(value/currency_info['USD/RUB'],2)}, "
                                     f"EUR : {round(value/currency_info['EUR/RUB'],2)}")


def usd(update, context):
    currency_info = {}
    text = update.message.text.split()
    value = float(text[1])
    url = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json?iss.meta=off'
    response = requests.get(url)
    currency_data = response.json()['securities']['data']
    for _x in currency_data:
        currency_info[_x[2]]=_x[3]
    return update.message.reply_text(f"RUB : {round(value*currency_info['USD/RUB'],2)}")


def eur(update, context):
    currency_info = {}
    text = update.message.text.split()
    value = float(text[1])
    url = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json?iss.meta=off'
    response = requests.get(url)
    currency_data = response.json()['securities']['data']
    for _x in currency_data:
        currency_info[_x[2]]=_x[3]
    return update.message.reply_text(f"RUB : {round(value*currency_info['EUR/RUB'],2)}")


