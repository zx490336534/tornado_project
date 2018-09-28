# coding=utf-8
# Auth:zx
# Time:2018/9/20 0020 22:33
from datetime import datetime
from sqlalchemy import (Column, Integer, String, DateTime, ForeignKey)
from .db import Base, DBSession
from sqlalchemy.sql import exists
from sqlalchemy.orm import relationship

# alembic revision --autogenerate -m 'create users table'

session = DBSession()


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True, nullable=False)
    # email = Column(String(50), unique=True, nullable=False)
    password = Column(String(50), nullable=False)
    created = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return '<User(#{}:{})>'.format(self.id, self.name)

    @classmethod
    def is_exists(cls, username):
        return session.query(exists().where(User.name == username)).scalar()

    @classmethod
    def add_user(cls, username, password):
        user = User(name=username, password=password)
        session.add(user)
        session.commit()

    @classmethod
    def get_pass(cls, username):
        user = session.query(cls).filter_by(name=username).first()
        if user:
            return user.password
        else:
            return ''


class Post(Base):
    """
    用户图片信息
    """
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    image_url = Column(String(80))
    thumb_url = Column(String(80))
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', backref='posts', uselist=False, cascade='all')

    def __repr__(self):
        return '<Post(#{})>'.format(self.id)


class Like(Base):
    """
    记录用户喜欢图片信息
    """
    __tablename__ = 'likes'

    user_id = Column(Integer,ForeignKey('users.id'),nullable=False,primary_key=True)
    post_id = Column(Integer,ForeignKey('posts.id'),nullable=False,primary_key=True)


if __name__ == '__main__':
    Base.metadata.create_all()
