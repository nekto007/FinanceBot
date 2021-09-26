import requests


def get_price(emitet):
    prices = dict()
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
