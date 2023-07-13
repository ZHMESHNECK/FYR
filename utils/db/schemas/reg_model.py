from utils.db.dbb import BaseModel
from sqlalchemy import Column, BigInteger, String, sql, Integer


class User_model(BaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    city = Column(String(25))
    min_price = Column(BigInteger)
    max_price = Column(BigInteger)
    count_rooms = Column(Integer)
    min_floor = Column(BigInteger)
    max_floor = Column(BigInteger)
    sort = Column(String(25))

    query: sql.select()
