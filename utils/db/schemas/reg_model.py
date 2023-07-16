from sqlalchemy import Column, BigInteger, String, sql, Integer
from utils.db.dbb import BaseModel


class User_model(BaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    city = Column(String(25), nullable=True)
    min_price = Column(BigInteger, nullable=True)
    max_price = Column(BigInteger, nullable=True)
    count_rooms = Column(Integer, nullable=True)
    min_floor = Column(Integer, nullable=True)
    max_floor = Column(Integer, nullable=True)
    sort = Column(String(25), nullable=True)

    query: sql.select()
