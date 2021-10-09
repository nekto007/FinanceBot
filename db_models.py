from sqlalchemy import Column, Integer, String, VARCHAR, Boolean, TIMESTAMP
from sqlalchemy.sql.functions import current_timestamp
from db_connect import Base, engine


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