import plotly.graph_objects as go
from datetime import datetime

# from db.db_connect import db_session
from models.db_models import StockHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///../identifier.sqlite', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))
emitet = 'TATN'
stock_scores = db_session.query(StockHistory.trade_date,
                                StockHistory.open_cost,
                                StockHistory.high_cost,
                                StockHistory.low_cost,
                                StockHistory.close_cost).filter(StockHistory.sec_id == 'TATN').all()

stocks_dict = {}
for row in stock_scores:
    dates, open_cost, high_cost, low_cost, close_cost = row[0], row[1], row[2], row[3], row[4]
    stocks_dict.setdefault("dates", []).append(dates)
    stocks_dict.setdefault("open_cost", []).append(open_cost/100)
    stocks_dict.setdefault("high_cost", []).append(high_cost/100)
    stocks_dict.setdefault("low_cost", []).append(low_cost/100)
    stocks_dict.setdefault("close_cost", []).append(close_cost/100)

fig = go.Figure(data=[go.Candlestick(x=stocks_dict['dates'],
                open=stocks_dict['open_cost'],
                high=stocks_dict['high_cost'],
                low=stocks_dict['low_cost'],
                close=stocks_dict['close_cost'])],
                layout=go.Layout(title=go.layout.Title(text=f'График движения цены эмитента {emitet}')))
fig.update_layout(xaxis_rangeslider_visible=False, xaxis=dict(type = 'category'))
fig.write_image("images/fig1.jpeg")
go.Figure()
