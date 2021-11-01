import requests
import datetime
from clients.client_info import post_client_info


def get_currency_api():
    currency_info = {}
    url = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json?iss.meta=off'
    response = requests.get(url)
    currency_data = response.json()['securities']['data']
    for _x in currency_data:
        currency_info[_x[2]] = _x[3]
    return currency_info


def get_all_currency(update, context):
    post_client_info(update, '')
    currency_array = get_currency_api()
    print(currency_array['USD/RUB'], currency_array['EUR/RUB'])
    update.message.reply_text(
        f'<b>Текущая дата: {datetime.datetime.now().date()}\n'
        f"Текущая котировка USD/RUB : {currency_array['USD/RUB']}\n"
        f"Текущая котировка EUR/RUB : {currency_array['EUR/RUB']}</b>\n",
        parse_mode='HTML')


def rub(update, context):
    currency_info = get_currency_api()
    text = update.message.text.split()
    value = float(text[1])
    return update.message.reply_text(f"USD : {round(value/currency_info['USD/RUB'],2)}, "
                                     f"EUR : {round(value/currency_info['EUR/RUB'],2)}")


def usd(update, context):
    currency_info = get_currency_api()
    text = update.message.text.split()
    value = float(text[1])
    return update.message.reply_text(f"RUB : {round(value*currency_info['USD/RUB'],2)}")


def eur(update, context):
    currency_info = get_currency_api()
    text = update.message.text.split()
    value = float(text[1])
    return update.message.reply_text(f"RUB : {round(value*currency_info['EUR/RUB'],2)}")


