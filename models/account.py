# coding=utf-8
# Auth:zx
# Time:2018/9/20 0020 22:33
from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime)
from .db import Base

#alembic revision --autogenerate -m 'create users table'

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id, self.name)


if __name__ == '__main__':
    Base.metadata.create_all()
