import requests
from auth import authorization
from datetime import datetime, timedelta
from db.db_connect import db_session
from models.db_models import StockInfo, Dividents, StockHistory, Calendar


# import prod


def get_price(emitet):
    url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json?iss.meta=off'
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
                stock_info = {'open_price': int(stock_data[9] * 100), 'close_price': int(stock_data[49] * 100),
                              'current_cost': int(stock_data[12] * 100), 'low_cost_daily': int(stock_data[10] * 100),
                              'high_cost_daily': int(stock_data[10] * 100), 'updated_at': datetime.now()}
                db_session.query(StockInfo).filter_by(sec_id=emitet).update(stock_info)
                db_session.commit()
            else:
                current_info = StockInfo(sec_id=stock_data[0], board_id='TQBR', open_price=int(stock_data[9] * 100)
                                         , close_price=int(stock_data[49] * 100),
                                         current_cost=int(stock_data[12] * 100),
                                         low_cost_daily=int(stock_data[10] * 100),
                                         high_cost_daily=int(stock_data[10] * 100)
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
    trade_list_dates = []
    date_ago = (datetime.now() - timedelta(days)).date()
    yesterday = (datetime.now() - timedelta(1)).date()
    working_date = db_session.query(Calendar.date).filter(Calendar.date >= str(date_ago),
                                                          Calendar.date <= str(yesterday)).all()
    trade_dates = db_session.query(StockHistory.trade_date).filter(StockHistory.sec_id == emitet,
                                                                   StockHistory.trade_date >= str(date_ago)).all()

    if len(working_date) != len(trade_dates):
        url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{emitet}' \
              f'.json?from={date_ago}&till={yesterday} '
        response = requests.get(url, cookies=authorization.get_auth()).json()
        history_data = response['history']['data']
        if len(history_data) != 0:
            for element in history_data:
                if element[1] not in trade_list_dates:
                    stock_history = StockHistory(board_id=element[0],
                                                 trade_date=element[1],
                                                 short_name=element[2], sec_id=element[3],
                                                 number_of_trades=int(element[4]),
                                                 value_trade=int(element[5]), open_cost=int(element[6] * 100),
                                                 low_cost=int(element[7] * 100), high_cost=int(element[8] * 100),
                                                 close_cost=int(element[9] * 100), created_at=datetime.now(),
                                                 updated_at=datetime.now()
                                                 )
                    db_session.add(stock_history)
                    try:
                        db_session.commit()
                    except:
                        db_session.rollback()
                        # ignore error
                        pass
        else:
            return None
    history_close_costs = db_session.query(StockHistory.close_cost).filter(StockHistory.sec_id == emitet,
                                                                           StockHistory.trade_date >= str(
                                                                               date_ago)).all()
    for history_close_cost in history_close_costs:
        history_price.append(history_close_cost[0] / 100)
    average['ticket_name'] = emitet
    average['company_name'] = db_session.query(StockHistory.short_name).filter(StockHistory.sec_id == emitet) \
        .first()[0]
    average['average'] = round(sum(history_price) / len(history_price), 3)
    db_session.close()
    return average


def get_date_dividents(emitet):
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
