from sqlalchemy import Column, Integer, String, VARCHAR, Boolean, TIMESTAMP
from db_connect import Base, engine
from datetime import datetime


class Authorization(Base):
    __tablename__= "auth"

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(VARCHAR)
    is_expired = Column(Boolean, default=False)
    stock_type = Column(Integer, default=1)
    created_at = Column(TIMESTAMP, nullable=False, default=datetime.now())
    updated_at = Column(TIMESTAMP, nullable=False, default=datetime.now())

    def __repr__(self):
        return f"{self.token}, {self.created_at}"

if __name__=="__main__":
    Base.metadata.create_all(bind=engine)