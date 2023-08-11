from sqlalchemy import Column, BigInteger, String, sql, Integer, DateTime
from typing import List
from gino import Gino
import sqlalchemy as sa

db = Gino()


class BaseModel(db.Model):
    __abstract__ = True

    def __str__(self):
        model = self.__class__.__name__
        table: sa.Table = sa.inspect(self.__class__)
        primary_key_columns: List[sa.Column] = table.primary_key.columns
        values = {
            column.name: getattr(self, self._column_name_map[column.name])
            for column in primary_key_columns
        }
        values_str = " ".join(
            f"{name}={value!r}" for name, value in values.items())
        return f"<{model} {values_str}>"


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
