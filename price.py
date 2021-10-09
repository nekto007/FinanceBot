import requests
from auth import authorization
from datetime import datetime, timedelta


def get_price(emitet):
    prices = {}
    authorization.is_cookie_expired(authorization.validation_cookie)  # Проверка текущего куки на валидность
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json?iss.meta=off'
    response = requests.get(url, cookies=authorization.validation_cookie).json()
    if len(response['marketdata']['data']) != 0:
        for i in response['marketdata']['data']:
            prices['ticket_name'] = i[0]
            prices['cost'] = i[12]
            prices['cost_open'] = i[9]
            prices['cost_close'] = i[49]
            prices['max_cost'] = i[11]
            prices['min_cost'] = i[10]
            return prices


def get_average(emitet, days):
    history_price = []
    average = {}
    authorization.is_cookie_expired(authorization.validation_cookie)  # Проверка текущего куки на валидность
    date_ago = (datetime.now() - timedelta(days)).strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{emitet}' \
          f'.json?from={date_ago}&till={yesterday} '
    response = requests.get(url, cookies=authorization.validation_cookie).json()
    history_data = response['history']['data']
    if len(history_data) != 0:
        for element in history_data:
            history_price.append(element[11])
        average['ticket_name'] = history_data[0][3]
        average['company_name'] = history_data[0][2]
        average[f'average'] = round(sum(history_price) / len(history_price), 3)
        return average


def get_date_dividents(emitet):
    dividents = {}
    authorization.is_cookie_expired(authorization.validation_cookie)  # Проверка текущего куки на валидность
    url = f'https://iss.moex.com/iss/securities/{emitet}/dividends.json'
    response = requests.get(url, cookies=authorization.validation_cookie).json()
    last_dividents = response['dividends']['data'][-1]
    if last_dividents[2] < str(datetime.now()):
        dividents['date_dividents'] = f'Дата выплаты последних дивидендов: {last_dividents[2]}, ' \
                                      f'на сумму: {last_dividents[3]} {last_dividents[4]} за акцию'
    else:
        dividents['date_dividents'] = f'Дата, до которой включительно необходимо купить акции для ' \
                                      f'получения диведендов: {last_dividents[2]}, ' \
                                      f'на сумму: {last_dividents[3]} {last_dividents[4]} за акцию'
    return dividents


if __name__ == "__main__":
    print(get_average('sber', 20))
    print(get_price('tatn'))
    print(get_date_dividents('tatn'))
