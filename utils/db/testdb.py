from utils.db.dbb import BaseModel
from sqlalchemy import Column, BigInteger,String, sql

class User(BaseModel):
    __tablename__ = 'users'
    user_id = Column(BigInteger, primary_key=True)
    city = Column(String(25),primary_key=True)

    query: sql.select()