from sqlalchemy import Column, ForeignKey, Integer, VARCHAR, Text, Date, DateTime, TIMESTAMP, Numeric, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import current_timestamp
from db.db_connect import Base, engine


class StockInfo(Base):
    __tablename__ = 'stock_info'
    __tableargs__ = {
        'comment': 'информация по акциям'
    }

    id = Column(Integer, autoincrement=True, comment='id')
    created_at = Column(TIMESTAMP, default=current_timestamp(), comment='Дата создания')
    updated_at = Column(TIMESTAMP, default=current_timestamp(), comment='Дата обновления')
    sec_id = Column(VARCHAR, nullable=False, comment='Идентификатор финансового инструмента', primary_key=True, unique=True)
    board_id = Column(VARCHAR, nullable=False, comment='Идентификатор режима торгов')
    open_price = Column(Numeric(2), comment='Цена открытия торгой')
    close_price = Column(Numeric(2), comment='Цена закрытия торгов')
    current_cost = Column(Numeric(2), comment='Текущая стоимость')
    low_cost_daily = Column(Numeric(2), comment='Минимальная цена сделки за день')
    high_cost_daily = Column(Numeric(2), comment='Максимальная цена сделки за день')

    def __repr__(self):
        return f'{self.sec_id}, {self.current_cost}, {self.open_price}, {self.close_price}, {self.high_cost_daily},' \
               f' {self.low_cost_daily}'

class StockHistory(Base):
    __tablename__ = 'stock_history'
    __tableargs__ = {
        'comment': 'исторические данные по акциям'
    }
    id = Column(Integer, autoincrement=True, primary_key=True)
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


class Authorization(Base): #Таблица авторизации
    __tablename__ = "auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(VARCHAR)
    is_expired = Column(Boolean, default=False)
    stock_type = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())

    def __repr__(self):
        return f"{self.token}, {self.created_at}"


class ClientStatus(Base): #Таблица client_status
    __tablename__ = "client_status"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(VARCHAR, nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.name}"


class Clients(Base): #Таблица clients
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_id = Column(VARCHAR)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    status = Column(Integer, default=1)
    is_deleted = Column(Boolean, default=False)
    username = Column(VARCHAR)

    def __repr__(self):
        return f"{self.id}, {self.telegram_id,}, {self.username}"


if __name__=="__main__":
    Base.metadata.create_all(bind=engine)
