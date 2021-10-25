import plotly.graph_objects as go
from datetime import (
    datetime,
    timedelta,
)
from db.db_connect import db_session
from db_models import StockHistory
from configs.settings import IMAGE_PATH


def get_candle(emitet, days):
    stocks_dict = {}
    date_ago = (datetime.now() - timedelta(days)).date()
    stock_scores = db_session.query(StockHistory.trade_date,
                                    StockHistory.open_cost,
                                    StockHistory.high_cost,
                                    StockHistory.low_cost,
                                    StockHistory.close_cost).filter(StockHistory.sec_id == emitet,
                                                                    StockHistory.trade_date >= str(date_ago)).all()
    if stock_scores:
        for row in stock_scores:
            dates, open_cost, high_cost, low_cost, close_cost = row
            stocks_dict.setdefault('dates', []).append(dates)
            stocks_dict.setdefault('open_cost', []).append(open_cost / 100)
            stocks_dict.setdefault('high_cost', []).append(high_cost / 100)
            stocks_dict.setdefault('low_cost', []).append(low_cost / 100)
            stocks_dict.setdefault('close_cost', []).append(close_cost / 100)
        fig = go.Figure(data=[go.Candlestick(x=stocks_dict['dates'],
                                             open=stocks_dict['open_cost'],
                                             high=stocks_dict['high_cost'],
                                             low=stocks_dict['low_cost'],
                                             close=stocks_dict['close_cost']
                                             )],
                        layout=go.Layout(title=go.layout.Title(text=f'График движения цены эмитента {emitet}')))
        fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(type='category'))
        fig.update_xaxes(tickangle=90)
        file_name = f'{IMAGE_PATH}/candle_{datetime.now().strftime("%s")}.jpeg'
        fig.write_image(file_name)
        go.Figure()
        return file_name


def get_graph(emitet, days):
    stocks_dict = {}
    date_ago = (datetime.now() - timedelta(days)).date()
    stock_scores = db_session.query(StockHistory.trade_date,
                                    StockHistory.close_cost).filter(StockHistory.sec_id == emitet,
                                                                    StockHistory.trade_date >= str(date_ago)).all()
    if stock_scores:
        for row in stock_scores:
            dates, close_cost = row[0], row[1]
            stocks_dict.setdefault('dates', []).append(dates)
            stocks_dict.setdefault('close_cost', []).append(close_cost / 100)
        sd = stocks_dict
        fig = go.Figure(data=[go.Scatter(x=sd["dates"], y=sd["close_cost"])],
                        layout=go.Layout(title=go.layout.Title(text=f'График движения цены эмитента {emitet}')))
        fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(type='category'))
        fig.update_xaxes(tickangle=90)
        file_name = f'{IMAGE_PATH}/graph_{datetime.now().strftime("%s")}.jpeg'
        fig.write_image(file_name)
        go.Figure()
        return file_name


if __name__ == '__main__':
    pass
