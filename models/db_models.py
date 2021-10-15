from sqlalchemy import create_engine
from sqlalchemy import Column, ForeignKey, INTEGER, VARCHAR, INTEGER, \
    TIMESTAMP, Numeric, Boolean, JSON, Date, DATETIME, Index
from sqlalchemy.sql.functions import current_timestamp, now
from db.db_connect import Base


class Authorization(Base):  # Таблица авторизации
    __tablename__ = "auth"

    id = Column(INTEGER, primary_key=True)
    token = Column(VARCHAR)
    is_expired = Column(Boolean, default=False)
    stock_type = Column(INTEGER, default=1)
    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())

    def __repr__(self):
        return f"{self.token}, {self.created_at}"


class Calendar(Base):  # Таблица client_status
    __tablename__ = "calendar"

    id = Column(INTEGER, primary_key=True)
    date = Column(VARCHAR, unique=True)

    def __repr__(self):
        return f"{self.id}, {self.date}"


class ClientStatus(Base):  # Таблица client_status
    __tablename__ = "client_status"

    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR, nullable=False)

    def __repr__(self):
        return f"{self.id}, {self.name}"


class Clients(Base):  # Таблица clients
    __tablename__ = "clients"

    id = Column(INTEGER, primary_key=True)
    telegram_id = Column(VARCHAR)
    first_name = Column(VARCHAR)
    last_name = Column(VARCHAR)
    created_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    updated_at = Column(TIMESTAMP, nullable=False, default=current_timestamp())
    status = Column(INTEGER, default=1)
    is_deleted = Column(Boolean, default=False)
    username = Column(VARCHAR)

    def __repr__(self):
        return f"{self.id}, {self.telegram_id,}, {self.username}"


class Dividents(Base):
    __tablename__ = "dividents"
    __tableargs__ = {'comment': 'Информация о дивидендах по акциям'
                     }

    id = Column(INTEGER, primary_key=True)
    created_at = Column(TIMESTAMP, nullable=False, default=now())
    updated_at = Column(TIMESTAMP, nullable=False, default=now())
    sec_id = Column(VARCHAR, nullable=False, comment='Идентификатор финансового инструмента')
    dividents_data = Column(JSON)

    def __repr__(self):
        return f"{self.updated_at},{self.dividents_data}"


class StockHistory(Base):
    __tablename__ = 'stock_history'
    __tableargs__ = {
        'comment': 'исторические данные по акциям'
    }
    __table_args__ = (Index('stock_history_sec_id_trade_date_uindex', 'sec_id', 'trade_date', unique=True),)
    id = Column(INTEGER, primary_key=True)
    created_at = Column(TIMESTAMP, default=now)
    updated_at = Column(TIMESTAMP, default=current_timestamp, comment='Дата обновления')
    sec_id = Column(VARCHAR, nullable=False, comment='Идентификатор финансового инструмента')
    board_id = Column(VARCHAR)
    short_name = Column(VARCHAR)
    trade_date = Column(VARCHAR)
    value_trade = Column(INTEGER)
    number_of_trades = Column(INTEGER)
    open_cost = Column(INTEGER)
    close_cost = Column(INTEGER)
    low_cost = Column(INTEGER)
    high_cost = Column(INTEGER)

    def __repr__(self):
        return f'{self.id}, {self.sec_id}'


class StockInfo(Base):
    __tablename__ = 'stock_info'
    __tableargs__ = {
        'comment': 'информация по акциям'
    }

    id = Column(INTEGER, primary_key=True, comment='id')
    created_at = Column(TIMESTAMP, default=current_timestamp(), comment='Дата создания')
    updated_at = Column(TIMESTAMP, default=current_timestamp(), comment='Дата обновления')
    sec_id = Column(VARCHAR, nullable=False, comment='Идентификатор финансового инструмента')
    board_id = Column(VARCHAR, nullable=False, comment='Идентификатор режима торгов')
    open_price = Column(INTEGER(), comment='Цена открытия торгой')
    close_price = Column(INTEGER(), comment='Цена закрытия торгов')
    current_cost = Column(INTEGER(), comment='Текущая стоимость')
    low_cost_daily = Column(INTEGER(), comment='Минимальная цена сделки за день')
    high_cost_daily = Column(INTEGER(), comment='Максимальная цена сделки за день')

    def __repr__(self):
        return f'{self.sec_id}, {self.current_cost}, {self.open_price}, {self.close_price}, {self.high_cost_daily},' \
               f' {self.low_cost_daily}'


class Trands(Base):
    __tablename__ = 'trands'
    __tableargs__ = {
        'comment': 'Тренды цены акций'
    }
    id = Column(INTEGER, primary_key=True)
    sec_id = Column(VARCHAR, nullable=False, comment='Идентификатор финансового инструмента')
    current_trand_days = Column(INTEGER, default=1)
    trand_status = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, default=current_timestamp, comment='Дата создания')
    updated_at = Column(INTEGER, default=current_timestamp, comment='Дата обновления')

    def __repr__(self):
        return f'{self.id}, {self.sec_id}'


if __name__ == "__main__":
    engine = create_engine('sqlite:///../identifier_test.sqlite', echo=True)
    Base.metadata.create_all(bind=engine)
