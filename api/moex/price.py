from datetime import (
    datetime,
    timedelta,
)

import requests
from sqlalchemy.exc import IntegrityError

from auth import authorization
from db.db_connect import db_session
from get_candles import (
    get_candle,
    get_graph,
)
from db_models import (
    Calendar,
    Dividents,
    StockHistory,
    StockInfo,
    StockTickers,
)


def get_price(emitet):
    price_info = {}
    all_tickers = get_all_tickers()
    if emitet in all_tickers:
        price_date = db_session.query(StockInfo.updated_at).filter(StockInfo.sec_id == emitet.upper()).first()
        if not (price_date is not None and (datetime.now() - price_date[0]).total_seconds() < 3600):
            url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json'
            parameters = {'iss.meta': 'off'}
            response = requests.get(url, params=parameters, cookies=authorization.get_auth()).json()
            stock_data = response['marketdata']['data']
            if len(stock_data):
                count_string = db_session.query(StockInfo, StockInfo.id).filter(
                    StockInfo.sec_id == emitet.upper()).count()
                if count_string:
                    if stock_data[0][9] is not None:
                        stock_info = {'open_price': int(stock_data[0][9] * 100),
                                      'close_price': int(stock_data[0][49] * 100),
                                      'current_cost': int(stock_data[0][12] * 100),
                                      'low_cost_daily': int(stock_data[0][10] * 100),
                                      'high_cost_daily': int(stock_data[0][11] * 100), 'updated_at': datetime.now()}
                        db_session.query(StockInfo).filter_by(sec_id=emitet).update(stock_info)
                        db_session.commit()
                    else:
                        return None
                else:
                    if stock_data[0][9] is not None:
                        current_info = StockInfo(sec_id=stock_data[0][0], board_id=stock_data[0][1],
                                                 short_name=response['securities']['data'][0][9],
                                                 open_price=int(stock_data[0][9] * 100),
                                                 close_price=int(stock_data[0][49] * 100),
                                                 current_cost=int(stock_data[0][12] * 100),
                                                 low_cost_daily=int(stock_data[0][10] * 100),
                                                 high_cost_daily=int(stock_data[0][11] * 100)
                                                 )
                        db_session.add(current_info)
                        db_session.commit()
                    else:
                        return None
            else:
                db_session.close()
                return None
        stock_info = db_session.query(StockInfo.current_cost, StockInfo.open_price,
                                      StockInfo.close_price, StockInfo.low_cost_daily,
                                      StockInfo.high_cost_daily, StockInfo.short_name) \
            .filter(StockInfo.sec_id == emitet.upper()).first()
        price_info['ticket_name'] = emitet
        price_info['current_cost'] = stock_info[0] / 100
        price_info['open_price'] = stock_info[1] / 100
        price_info['close_price'] = stock_info[2] / 100
        price_info['low_cost_daily'] = stock_info[3] / 100
        price_info['high_cost_daily'] = stock_info[4] / 100
        price_info['company_name'] = stock_info[5]
        if get_stock_history(emitet, 15) is not None:
            price_info['graph_photo'] = get_graph(emitet, 15)
        else:
            price_info['graph_photo'] = None
        db_session.close()
        return price_info


def get_average(emitet, days):
    all_tickers = get_all_tickers()
    if emitet in all_tickers:
        history_price = []
        average = {}

        date_ago = (datetime.now() - timedelta(days)).date()
        yesterday = (datetime.now() - timedelta(1)).date()
        working_date = db_session.query(Calendar.date).filter(Calendar.date >= str(date_ago),
                                                              Calendar.date <= str(yesterday)).all()
        trade_dates = db_session.query(StockHistory.trade_date).filter(StockHistory.sec_id == emitet,
                                                                       StockHistory.trade_date >= str(date_ago)).all()

        if len(working_date) != len(trade_dates):
            stock_history = get_stock_history(emitet, days)
            if stock_history is None:
                db_session.close()
                return None
        history_close_costs = db_session.query(StockHistory.close_cost).filter(StockHistory.sec_id == emitet,
                                                                               StockHistory.trade_date >= str(
                                                                                   date_ago)).all()
        history_price = [history_close_cost[0] / 100 for history_close_cost in history_close_costs]
        average['ticket_name'] = emitet
        average['company_name'] = \
            db_session.query(StockHistory.short_name).filter(StockHistory.sec_id == emitet.upper()) \
                .first()[0]
        average['average'] = round(sum(history_price) / len(history_price), 3)
        average['candle_photo'] = get_candle(emitet, days)
        db_session.close()
        return average


def get_stock_history(emitet, days):
    trade_list_dates = []
    date_ago = (datetime.now() - timedelta(days)).date()
    yesterday = (datetime.now() - timedelta(1)).date()
    url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json?'
    parameters = {'from': date_ago, 'till': yesterday}
    response = requests.get(url, params=parameters, cookies=authorization.get_auth()).json()
    history_data = response['history']['data']
    if len(history_data) != 0:
        for element in history_data:
            if element[1] not in trade_list_dates and element[6] is not None:
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
                except IntegrityError:
                    db_session.rollback()
    else:
        db_session.close()
        return None
    db_session.close()
    return True


def get_date_dividents(emitet):
    dividents_date = db_session.query(Dividents.updated_at).filter(Dividents.sec_id == emitet.upper()).all()
    len_dividents_date = len(dividents_date)
    if len_dividents_date and dividents_date == datetime.now().date():
        dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet.upper()).all()
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
    dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet.upper())
    db_session.close()
    return dividents_info[0][0]


def get_all_tickers(emitet=''):
    if not emitet:
        price_date = db_session.query(StockTickers.updated_at).filter(StockTickers.name_stock == 'MOEX').first()
    else:
        price_date = db_session.query(StockTickers.updated_at).filter(StockTickers.name_stock == 'MOEX',
                                                                      StockTickers.sec_id == emitet.upper()).first()
    if not (price_date is not None and (datetime.now() - price_date[0]).total_seconds() < 86400):
        url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities.json'
        parameters = {'iss.meta': 'off'}
        response = requests.get(url, params=parameters, cookies=authorization.get_auth()).json()
        tickers_data = response['securities']['data']
        for ticker in tickers_data:
            if price_date is not None and ticker[0] in price_date:
                current_info = {'sec_id': ticker[0],
                                'updated_at': datetime.now().date()}
                db_session.query(Dividents).filter_by(sec_id=emitet).update(current_info)
            else:
                current_info = StockTickers(sec_id=ticker[0],
                                            company_name=ticker[9],
                                            name_stock='MOEX'
                                            )
                db_session.add(current_info)
            try:
                db_session.commit()
            except IntegrityError:
                db_session.rollback()
    if not emitet:
        tickers_info = []
        tickers_data = db_session.query(StockTickers.sec_id).all()
        for ticker in tickers_data:
            tickers_info.append(ticker[0])
        return tickers_info
    else:
        tickers_info = db_session.query(StockTickers.sec_id, StockTickers.company_name, StockTickers.name_stock) \
            .filter(StockTickers.sec_id == emitet.upper()).all()
        if not len(tickers_info):
            return None
        db_session.close()
        return tickers_info


def get_currency_api():
    currency_info = {}
    url = 'https://iss.moex.com/iss/statistics/engines/futures/markets/indicativerates/securities.json?iss.meta=off'
    response = requests.get(url)
    currency_data = response.json()['securities']['data']
    for _x in currency_data:
        currency_info[_x[2]] = _x[3]
    return currency_info


if __name__ == "__main__":
    print(get_price('SBER'))
