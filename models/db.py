#coding=utf-8
#Auth:zx
#Time:2018/9/20 0020 22:30
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'tudo'
USERNAME = 'root'
PASSWORD = '123456'
DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOST,PORT,DATABASE)

engine = create_engine(DB_URI)
DBSession = sessionmaker(bind=engine)
Base = declarative_base(engine)