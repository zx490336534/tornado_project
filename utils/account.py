# coding=utf-8
# Auth:zx
# Time:2018/9/20 0020 21:46
import hashlib

from models.account import User, Post, Like


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


def authenticate(username, password, db_session):
    """
    校验用户名和密码是否符合记录
    :param username:
    :param password:
    :return:
    """
    if username and password:
        hashed_password = User.get_pass(username, db_session)
        return hashed(password) == hashed_password
    else:
        return False


def register(username, password):
    if User.is_exists(username):
        return {'msg': 'username is exists'}
    hash_pass = hashed(password)
    User.add_user(username, hash_pass)
    return {'msg': 'ok'}


class HandlerORM:
    """
    和 RequestHandler配合使用的数据库连接工具类
    """

    def __init__(self, db_session, username):
        """

        :param db_session: 由RequestHandler来调用并初始化和传入session 和执行session.close()
        :param username: pycket session记录的名字
        """
        self.db = db_session
        self.username = username

    def add_post_for_user(self, image_url, thumb_url):
        user = self.get_user()
        post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
        self.db.add(post)
        self.db.commit()
        return post

    def get_post_for_user(self):
        user = self.get_user()
        if user:
            return user.posts
        else:
            return []

    def get_post(self, post_id):
        post = self.db.query(Post).filter_by(id=post_id).first()
        return post

    def get_all_posts(self):
        posts = self.db.query(Post).order_by(Post.id.desc()).all()
        return posts

    def get_user(self):
        """
        由用户名获取对应记录
        :return:
        """
        user = self.db.query(User).filter_by(name=self.username).first()
        return user

    def get_like_posts(self, user):
        """
        查询用户喜欢的图片 posts
        :param user:User的实例
        :return:
        """
        posts = self.db.query(Post).filter(Like.user_id == user.id,
                                           Post.id == Like.post_id,
                                           Post.user_id != user.id).all()
        return posts

    def get_like_count(self, post):
        count = self.db.query(Like).filter_by(post_id=post.id).count()
        return count
