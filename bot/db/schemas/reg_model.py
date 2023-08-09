from sqlalchemy import Column, BigInteger, String, sql, Integer, DateTime
from db.schemas.dbb import BaseModel


class User_model(BaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True, nullable=False)
    city = Column(String(25), nullable=True)
    min_price = Column(BigInteger, nullable=True)
    max_price = Column(BigInteger, nullable=True)
    count_rooms = Column(String(3), nullable=True)
    min_floor = Column(Integer, nullable=True)
    max_floor = Column(Integer, nullable=True)
    sort = Column(String(25), nullable=True)
    time = Column(DateTime(timezone=False))

    query: sql.select()
