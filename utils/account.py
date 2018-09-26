# coding=utf-8
# Auth:zx
# Time:2018/9/20 0020 21:46
import hashlib

from models.account import User, session, Post


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


def authenticate(username, password):
    """
    校验用户名和密码是否符合记录
    :param username:
    :param password:
    :return:
    """
    if username and password:
        hashed_password = User.get_pass(username)
        return hashed(password) == hashed_password
    else:
        return False


def register(username, password):
    if User.is_exists(username):
        return {'msg': 'username is exists'}
    hash_pass = hashed(password)
    User.add_user(username, hash_pass)
    return {'msg': 'ok'}


def add_post(username, image_url, thumb_url):
    """
    保存用户上传的图片信息
    :return:
    """
    user = session.query(User).filter_by(name=username).first()
    post = Post(image_url=image_url, thumb_url=thumb_url, user=user)
    session.add(post)
    session.commit()
    return post

def get_post_for(username):
    user = session.query(User).filter_by(name=username).first()
    if user:
        return user.posts
    else:
        return []

def get_post(post_id):
    post = session.query(Post).filter_by(id=post_id).first()
    return post

def get_all_posts():
    posts = session.query(Post).order_by(Post.id.desc()).all()
    return posts