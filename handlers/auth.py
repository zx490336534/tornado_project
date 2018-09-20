# coding=utf-8
# Auth:zx
# Time:2018/9/20 0020 21:35

import tornado.web
from .main import AuthBaseHandler
from utils.account import authenticate

class LoginHandler(AuthBaseHandler):
    """
    登陆接口
    """

    def get(self, *args, **kwargs):
        self.render('login.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)

        passed = authenticate(username,password)
        if passed:
            self.session.set('tudo_user_info',username)#与main中的get('tudo_user_info')对应
            self.redirect('/')
        else:
            self.write('login fail')
