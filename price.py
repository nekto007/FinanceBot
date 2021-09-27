import requests
from datetime import datetime, timedelta


def get_price(emitet):
    prices = {}
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/securities/{emitet}.json?iss.meta=off'
    response = requests.get(url).json()
    if len(response['marketdata']['data']) != 0:
        prices['ticket_name'] = response['marketdata']['data'][2][0]
        prices['cost'] = response['marketdata']['data'][2][12]
        prices['cost_open'] = response['marketdata']['data'][2][9]
        prices['cost_close'] = response['marketdata']['data'][2][23]
        prices['max_cost'] = response['marketdata']['data'][2][11]
        prices['min_cost'] = response['marketdata']['data'][2][10]
        return prices


def get_average(emitet, days):
    history_price = []
    average = {}
    date_ago = (datetime.now() - timedelta(days)).strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{emitet}' \
          f'.json?from={date_ago}&till={yesterday} '
    response = requests.get(url).json()
    history_data = response['history']['data']
    if len(history_data) != 0:
        for element in history_data:
            history_price.append(element[11])
        average['ticket_name'] = history_data[0][3]
        average['company_name'] = history_data[0][2]
        average[f'average'] = round(sum(history_price) / len(history_price), 3)
        return average

if __name__ == '__main__':
    pass