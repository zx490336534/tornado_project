# coding=utf-8
# Auth:zx
# Time:2018/9/20 0020 21:35
import tornado.web
from .main import AuthBaseHandler
from utils.account import authenticate, register


class LoginHandler(AuthBaseHandler):
    """
    登陆接口
    """

    def get(self, *args, **kwargs):
        next_url = self.get_argument('next', '/')
        self.render('login.html', next_url=next_url, error=None)

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        next_url = self.get_argument('next', '/')

        passed = authenticate(username, password)

        if passed:
            self.session.set('tudo_user_info', username)  # 与main中的get('tudo_user_info')对应
            self.redirect(next_url)
        else:
            self.write('login fail')


class LogoutHandler(AuthBaseHandler):
    """
    登出接口
    """

    def get(self, *args, **kwargs):
        self.session.delete('tudo_user_info')
        self.redirect('/login')


class SignupHandler(AuthBaseHandler):
    """
    注册创建用户
    """

    def get(self, *args, **kwargs):
        self.render('signup.html', msg='')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        if username and password1 and password2:
            if password1 != password2:
                self.write({'msg': '两次输入的密码不匹配！'})
            else:
                ret = register(username, password1)
                if ret['msg'] == 'ok':
                    self.session.set('tudo_user_info', username)
                    self.redirect('/')
                else:
                    self.write(ret)
        else:
            self.render('signup.html', msg={'register fail'})



