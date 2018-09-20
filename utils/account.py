#coding=utf-8
#Auth:zx
#Time:2018/9/20 0020 21:46
import hashlib



def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

USER_DATA = {
    "name":"tudo",
    "password":hashed("123")
}

def authenticate(username,password):
    """
    校验用户名和密码是否符合记录
    :param username:
    :param password:
    :return:
    """
    if username and password:
        return (username == USER_DATA['name']) and (hashed(password) == USER_DATA['password'])
    else:
        return False