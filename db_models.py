from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, Text, Date, DateTime, TIMESTAMP, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp

Base = declarative_base()


class StockInfo(Base):
    __tablename__ = 'stock_info'
    __tableargs__ = {
        'comment': 'информация по акциям'
    }

    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    created_at = Column(TIMESTAMP, default=current_timestamp, comment='Дата создания')
    updated_at = Column(Integer, default=current_timestamp, comment='Дата обновления')
    sec_id = Column(VARCHAR, nullable=False, comment='Идентификатор финансового инструмента', primary_key=True)
    board_id = Column(VARCHAR, nullable=False, comment='Идентификатор режима торгов')
    open_price = Column(Numeric, comment='Цена открытия торгой')
    close_price = Column(Numeric, comment='Цена закрытия торгов')
    current_cost = Column(Numeric, comment='Текущая стоимость')
    low_cost_daily = Column(Numeric, comment='Минимальная цена сделки за день')
    high_cost_daily = Column(Numeric, comment='Максимальная цена сделки за день')

    def __repr__(self):
        return f'{self.id}, {self.sec_id}'


class StockHistory(Base):
    __tablename__ = 'stock_history'
    __tableargs__ = {
        'comment': 'исторические данные по акциям'
    }
    id = Column(Integer, autoincrement=True)
    created_at = Column(TIMESTAMP, default=current_timestamp, comment='Дата создания')
    updated_at = Column(Integer, default=current_timestamp, comment='Дата обновления')
    sec_id = Column(Integer, ForeignKey('stock_info.id'))
    board_id = Column(VARCHAR)
    short_name = Column(VARCHAR)
    trade_date = Column(TIMESTAMP)
    value_trade = Column(Numeric)
    number_of_trades = Column(Integer)
    open_cost = Column(Numeric)
    close_cost = Column(Numeric)
    low_cost = Column(Numeric)
    high_cost = Column(Numeric)

    def __repr__(self):
        return f'{self.id}, {self.sec_id}'


class Trands(Base):
    __tablename__ = 'trands'
    __tableargs__ = {
        'comment': 'Тренды цены акций'
    }
    id = Column(Integer, primary_key=True, autoincrement=True)
    sec_id = Column(Integer, ForeignKey('stock_info.id'))
    current_trand_days = Column(Integer, default=1)
    trand_status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=current_timestamp, comment='Дата создания')
    updated_at = Column(Integer, default=current_timestamp, comment='Дата обновления')

    def __repr__(self):
        return f'{self.id}, {self.sec_id}'


if __name__ == "__main__":
    pass
