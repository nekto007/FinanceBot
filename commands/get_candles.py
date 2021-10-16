import plotly.graph_objects as go
from datetime import datetime

# import finplot as fplt
# import yfinance

# from db.db_connect import db_session
from models.db_models import StockHistory
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

engine = create_engine('sqlite:///../identifier.sqlite', echo=True)
db_session = scoped_session(sessionmaker(bind=engine))

stock_scores = db_session.query(StockHistory.trade_date, StockHistory.open_cost, StockHistory.high_cost, StockHistory.low_cost,
                         StockHistory.close_cost).filter(StockHistory.sec_id == 'TATN').all()
dates = []
open_cost = []
high_cost = []
low_cost = []
close_cost = []
for stock in stock_scores:
    dates.append(stock[0])
    open_cost.append(stock[1])
    high_cost.append(stock[2])
    low_cost.append(stock[3])
    close_cost.append(stock[4])
# print(dates, open_cost, high_cost, low_cost, close_cost)
fig = go.Figure(data=[go.Candlestick(x=dates,
                open=open_cost,
                high=high_cost,
                low=low_cost,
                close=close_cost)])

fig.show()
