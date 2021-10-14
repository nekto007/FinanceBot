import requests
from auth import authorization
from datetime import datetime, timedelta
from db.db_connect import db_session
from models.db_models import StockInfo, Dividents


def get_price(emitet):
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json?iss.meta=off'
    # authorization.is_cookie_expired(authorization.get_auth())  # Проверка текущего куки на валидность
    price_date = db_session.query(StockInfo.updated_at).filter(StockInfo.sec_id == emitet).all()
    len_price_date = len(price_date)
    if len_price_date and (datetime.now() - price_date[0][0]).total_seconds() < 3600:
        pass
    else:
        response = requests.get(url, cookies=authorization.get_auth()).json()
        stock_data = response['marketdata']['data']
        if len(stock_data):
            count_string = db_session.query(StockInfo, StockInfo.id).filter(StockInfo.sec_id == emitet).count()
            if count_string:
                stock_info = {'open_price': int(stock_data[9]*100), 'close_price': int(stock_data[49]*100),
                              'current_cost': int(stock_data[12]*100), 'low_cost_daily': int(stock_data[10]*100),
                              'high_cost_daily': int(stock_data[10]*100), 'updated_at': datetime.now()}
                db_session.query(StockInfo).filter_by(sec_id=emitet).update(stock_info)
                db_session.commit()
            else:
                current_info = StockInfo(sec_id=stock_data[0], board_id='TQBR', open_price=int(stock_data[9]*100)
                                         , close_price=int(stock_data[49]*100), current_cost=int(stock_data[12]*100),
                                         low_cost_daily=int(stock_data[10]*100), high_cost_daily=int(stock_data[10]*100)
                                         )
                db_session.add(current_info)
                db_session.commit()
        else:
            return None
    stock_info = db_session.query(StockInfo.sec_id, StockInfo.current_cost, StockInfo.open_price,
                                  StockInfo.close_price, StockInfo.high_cost_daily,
                                  StockInfo.low_cost_daily).filter(StockInfo.sec_id == emitet).first()
    return stock_info


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
    len_dividents_date = len(dividents_date)
    if len_dividents_date and dividents_date == datetime.now().date():
        dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet).all()
        return dividents_info[0][0]
    url = f'https://iss.moex.com/iss/securities/{emitet}/dividends.json'
    response = requests.get(url, cookies=authorization.get_auth()).json()
    dividents = response['dividends']['data']
    if len_dividents_date and dividents:
        current_info = {'dividents_data': dividents,
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
