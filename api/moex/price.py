from datetime import (
    datetime,
    timedelta,
)

import requests
from sqlalchemy import (
    desc,
)
from sqlalchemy.exc import IntegrityError

from auth import authorization
from db.db_connect import db_session
from db_models import (
    Calendar,
    Dividents,
    StockHistory,
    StockInfo,
    StockTickers,
    Trands,
)
from get_candles import (
    get_graph,
)


def get_working_days():
    working_days_list = []
    calendar = db_session.query(Calendar.date).all()
    for day in calendar:
        working_days_list.append(day[0])
    return working_days_list


def get_previous_working_day():
    previous_working_day = db_session.query(Calendar.date).filter(Calendar.date < str(datetime.now().date())) \
        .order_by(desc(Calendar.date)).limit(1).first()[0]
    return previous_working_day


def get_average(emitet, days):
    all_tickers = get_all_tickers()
    if emitet in all_tickers:
        date_ago = (datetime.now() - timedelta(days)).date()
        yesterday = (datetime.now() - timedelta(1)).date()
        working_date = db_session.query(Calendar.date).filter(Calendar.date >= str(date_ago),
                                                              Calendar.date <= str(yesterday)).all()
        trade_dates = db_session.query(StockHistory.trade_date).filter(StockHistory.sec_id == emitet,
                                                                       StockHistory.trade_date >= str(date_ago)).all()
        if len(working_date) != len(trade_dates):
            stock_history = get_stock_history(emitet, date_ago)
            if stock_history is None:
                db_session.close()
                return None
        history_close_costs = db_session.query(StockHistory.close_cost, StockHistory.short_name) \
            .filter(StockHistory.sec_id == emitet, StockHistory.trade_date >= str(date_ago)).all()
        history_price = [history_close_cost[0] / 100 for history_close_cost in history_close_costs]
        short_name = db_session.query(StockHistory.short_name).filter(StockHistory.sec_id == emitet).first()[0]
        db_session.close()
        return history_price, short_name


def get_price(emitet):
    all_tickers = get_all_tickers()
    if emitet in all_tickers:
        price_date = db_session.query(StockInfo.updated_at).filter(StockInfo.sec_id == emitet.upper()).first()
        if not (price_date is not None and (datetime.now() - price_date[0]).total_seconds() < 3600):
            url = f'https://iss.moex.com/iss/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json'
            parameters = {'iss.meta': 'off'}
            response = requests.get(url, params=parameters, cookies=authorization.get_auth()).json()
            stock_data = response['marketdata']['data'][0]
            if stock_data[31] != 'B' and stock_data[9] is not None:
                close_price = stock_data[49]
                if close_price is None:
                    last_working_day = get_previous_working_day()
                    stock_history = get_stock_history(emitet, last_working_day)
                    if stock_history:
                        close_price = db_session.query(StockHistory.close_cost) \
                            .filter(StockHistory.sec_id == emitet,
                                    StockHistory.trade_date == last_working_day).first()[0]
                else:
                    close_price = int(close_price * 100)
                if price_date:
                    stock_info = {
                        'open_price': int(stock_data[9] * 100), 'close_price': close_price,
                        'current_cost': int(stock_data[12] * 100), 'low_cost_daily': int(stock_data[10] * 100),
                        'high_cost_daily': int(stock_data[11] * 100), 'updated_at': datetime.now()}
                    db_session.query(StockInfo).filter_by(sec_id=emitet.upper()).update(stock_info)
                    db_session.commit()
                else:
                    current_info = StockInfo(
                        sec_id=stock_data[0], board_id=stock_data[1], short_name=response['securities']['data'][9],
                        open_price=int(stock_data[9] * 100), close_price=close_price,
                        current_cost=int(stock_data[12] * 100), low_cost_daily=int(stock_data[10] * 100),
                        high_cost_daily=int(stock_data[11] * 100), updated_at=datetime.now(),
                        created_at=datetime.now())
                    db_session.add(current_info)
                    db_session.commit()
            else:
                db_session.close()
                return 'Нет сделок'
        stock_info = db_session.query(
            StockInfo.sec_id, StockInfo.current_cost, StockInfo.open_price, StockInfo.close_price,
            StockInfo.low_cost_daily, StockInfo.high_cost_daily, StockInfo.short_name) \
            .filter(StockInfo.sec_id == emitet.upper()).first()
        db_session.close()
        return stock_info


def get_stock_history(emitet, date_ago):
    trade_list_dates = []
    yesterday = (datetime.now() - timedelta(1)).date()
    url = f'https://iss.moex.com/iss/history/engines/stock/markets/shares/boards/TQBR/securities/{emitet}.json?'
    parameters = {'from': date_ago, 'till': yesterday}
    response = requests.get(url, params=parameters, cookies=authorization.get_auth()).json()
    history_data = response['history']['data']
    if len(history_data) != 0:
        for element in history_data:
            if element[1] not in trade_list_dates and element[6] is not None:
                stock_history = StockHistory(
                    board_id=element[0], trade_date=element[1], short_name=element[2], sec_id=element[3],
                    number_of_trades=int(element[4]), value_trade=int(element[5] * 100),
                    open_cost=int(element[6] * 100), low_cost=int(element[7] * 100), high_cost=int(element[8] * 100),
                    close_cost=int(element[9] * 100), created_at=datetime.now(), updated_at=datetime.now()
                )
                db_session.add(stock_history)
                try:
                    db_session.commit()
                except IntegrityError:
                    db_session.rollback()
                db_session.close()
            else:
                return None
        return True


def get_date_dividents(emitet):
    dividents_date = db_session.query(Dividents.updated_at).filter(Dividents.sec_id == emitet.upper()).first()
    if dividents_date and datetime.strftime(dividents_date[0], '%Y-%m-%d') == str(datetime.now().date()):
        dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet.upper()).first()
        return dividents_info[0]
    url = f'https://iss.moex.com/iss/securities/{emitet}/dividends.json'
    response = requests.get(url, cookies=authorization.get_auth()).json()
    dividents = response['dividends']['data']
    if dividents:
        if dividents_date:
            current_info = {'dividents_data': dividents,
                            'updated_at': datetime.now()}
            db_session.query(Dividents).filter_by(sec_id=emitet).update(current_info)
            db_session.commit()
        else:
            current_info = Dividents(sec_id=emitet, dividents_data=dividents,
                                     created_at=datetime.now(), updated_at=datetime.now())
            db_session.add(current_info)
            db_session.commit()
        dividents_info = db_session.query(Dividents.dividents_data).filter(Dividents.sec_id == emitet.upper()).first()
        db_session.close()
        return dividents_info[0]


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


def get_trand(emitet):
    is_emitet = db_session.query(Trands.trand_date).filter(Trands.sec_id == emitet)
    if is_emitet.count() and is_emitet[0][0] == str(datetime.now().date()):
        trand = db_session.query(
            Trands.sec_id,
            Trands.trand_status,
            Trands.current_trand_days,
            Trands.average_15, Trands.average_50) \
            .filter(Trands.sec_id == emitet).first()
        return trand
    ago_150_days = datetime.now().date() - timedelta(days=150)
    get_status_history = get_stock_history(emitet, ago_150_days)
    current_trand_days = 0
    if get_status_history:
        last_100_days_history = db_session.query(StockHistory.close_cost, StockHistory.trade_date) \
            .order_by(desc(StockHistory.trade_date)) \
            .filter(StockHistory.sec_id == emitet).limit(100).all()
        start_50_days = -1
        end_50_days = 50
        start_15_days = 50
        end_15_days = 64
        while start_15_days > -1:
            is_trand = False
            history_price = [history_trade_date[0]
                             for history_trade_date in last_100_days_history[start_50_days:end_50_days:-1]]
            history_50_price_sum = round((sum(history_price) / 100) / len(history_price), 3)
            history_price = [history_trade_date[0]
                             for history_trade_date in last_100_days_history[start_15_days:end_15_days:]]
            history_15_price_sum = round((sum(history_price) / 100) / len(history_price), 3)
            if history_15_price_sum > history_50_price_sum:
                is_trand = True
            trand_info = db_session.query(Trands.current_trand_days, Trands.trand_status) \
                .filter(Trands.sec_id == emitet).first()
            if not trand_info:
                current_trand_days = 1
                trand_status = Trands(sec_id=emitet, current_trand_days=current_trand_days,
                                      trand_status=is_trand,
                                      trand_date=datetime.now().date(),
                                      created_at=datetime.now(),
                                      updated_at=datetime.now(),
                                      average_15=history_15_price_sum,
                                      average_50=history_50_price_sum, )
                db_session.add(trand_status)
                db_session.commit()
            else:
                if trand_info[1] == is_trand:
                    current_trand_days += 1
                else:
                    current_trand_days = 0
                trand_status = {'sec_id': emitet,
                                # 'current_trand_days': current_trand_days,
                                'trand_status': is_trand,
                                'trand_date': datetime.now().date(),
                                'updated_at': datetime.now(),
                                'average_15': history_15_price_sum,
                                'average_50': history_50_price_sum}
                db_session.query(Trands).filter_by(sec_id=emitet).update(trand_status)
                db_session.commit()
            start_50_days -= 1
            end_50_days -= 1
            start_15_days -= 1
            end_15_days -= 1
    trand_days = {'current_trand_days': current_trand_days}
    db_session.query(Trands).filter_by(sec_id=emitet).update(trand_days)
    db_session.commit()
    trand = db_session.query(
        Trands.sec_id,
        Trands.trand_status,
        Trands.current_trand_days,
        Trands.average_15, Trands.average_50) \
        .filter(Trands.sec_id == emitet).first()
    return trand


if __name__ == "__main__":
    pass
