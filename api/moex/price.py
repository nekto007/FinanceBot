import requests

from auth import authorization
from sqlalchemy import select
from datetime import datetime, timedelta
from db.db_connect import db_session
from models.db_models import StockInfo, Dividents


def get_price(emitet):
    prices = {}
    # authorization.is_cookie_expired(authorization.get_auth())  # Проверка текущего куки на валидность
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json?iss.meta=off'
    response = requests.get(url, cookies=authorization.get_auth()).json()
    if len(response['marketdata']['data']) != 0:
        for i in response['marketdata']['data']:
            count_string = db_session.query(StockInfo, StockInfo.id).filter(StockInfo.sec_id == emitet).count()
            if count_string > 0:
                current_info = {'open_price': i[9], 'close_price': i[49],
                                'current_cost': i[12], 'low_cost_daily': i[10], 'high_cost_daily': i[10],
                                'updated_at': datetime.utcnow()}
                db_session.query(StockInfo).filter_by(sec_id=emitet).update(current_info)
                db_session.commit()
            else:
                current_info = StockInfo(sec_id=i[0], board_id='TQBR', open_price=i[9], close_price=i[49],
                                         current_cost=i[12], low_cost_daily=i[10], high_cost_daily=i[10])
                db_session.add(current_info)
                db_session.commit()
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
    # authorization.is_cookie_expired(authorization.get_auth())  # Проверка текущего куки на валидность
    date_ago = (datetime.now() - timedelta(days)).strftime("%Y-%m-%d")
    yesterday = (datetime.now() - timedelta(1)).strftime("%Y-%m-%d")
    url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{emitet}' \
          f'.json?from={date_ago}&till={yesterday} '
    response = requests.get(url, cookies=authorization.get_auth()).json()
    history_data = response['history']['data']
    if len(history_data) != 0:
        for element in history_data:
            history_price.append(element[11])
        average['ticket_name'] = history_data[0][3]
        average['company_name'] = history_data[0][2]
        average[f'average'] = round(sum(history_price) / len(history_price), 3)
        return average


def get_date_dividents(emitet):
    # authorization.is_cookie_expired(authorization.get_auth())  # Проверка текущего куки на валидность
    dividents_date = db_session.query(Dividents.updated_at).filter(Dividents.sec_id == emitet).all()
    count_string = len(dividents_date)
    if count_string > 0 and dividents_date == datetime.now().date():
        dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet)
        return dividents_info[0][0]
    url = f'https://iss.moex.com/iss/securities/{emitet}/dividends.json'
    response = requests.get(url, cookies=authorization.get_auth()).json()
    dividents = response['dividends']['data']
    if count_string > 0:
        current_info = {'sec_id': emitet,
                        'dividents_data': dividents,
                        'updated_at': datetime.now().date()}
        db_session.query(Dividents).filter_by(sec_id=emitet).update(current_info)
        db_session.commit()
    elif dividents:
        current_info = Dividents(sec_id=emitet, dividents_data=dividents)
        db_session.add(current_info)
        db_session.commit()
    else:
        return None
    dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet)
    return dividents_info[0][0]


if __name__ == "__main__":
    pass
