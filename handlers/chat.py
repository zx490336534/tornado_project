# coding=utf-8
# Auth:zx
# Time:2018/10/9 0009 21:25
import uuid

import tornado.web
import tornado.websocket
import tornado.httpclient
from .main import AuthBaseHandler
import tornado.escape
from tornado.ioloop import IOLoop
from pycket.session import SessionMixin


def make_chat(msg, img_url=None):
    """
    生成一个用来格式化 message.html的dict
    :param msg:
    :param img:
    :return:
    """
    ret = {
        'id': str(uuid.uuid4()),
        'body': msg,
        'img_url': img_url,
    }
    return ret


class RoomHanlder(AuthBaseHandler):
    """
    聊天室页面
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('room.html', messages=ChatSocketHandler.cache)


class ChatSocketHandler(tornado.websocket.WebSocketHandler, SessionMixin):
    """
    处理响应 websocker 连接
    """
    waiters = set()  # 等待接收信息的用户
    cache = []  # 存放消息
    cache_size = 200  # 消息列表的大小

    def get_current_user(self):
        return self.session.get('tudo_user_info')

    def open(self, *args, **kwargs):
        """新的WebSocket连接打开，自动调用"""
        print('new connetcon :%s' % self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """WebSocket连接断开，自动调用"""
        print('close connetcion: %s' % self)
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls, chat):
        """更新消息列表，加入新的消息"""
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls, chat):
        """给每个等待接收的用户发送新的消息"""
        for waiter in cls.waiters:
            waiter.write_message(chat)

    def on_message(self, message):
        """WebSocket 服务端接收到消息，自动调用"""
        print('got message :%s' % message)
        parese = tornado.escape.json_decode(message)
        if parese['body'] and parese['body'].startswith('http://'):
            # url = 'http://source.unsplash.com/random'
            url = parese['body']
            client = tornado.httpclient.AsyncHTTPClient()
            # http://123.56.13.233:8000/save?url=http://source.unsplash.com/random&user=zx&from=room
            save_api_url = f"http://127.0.0.1:8000/save?url={url}&user={self.current_user}&from=room"
            IOLoop.current().spawn_callback(client.fetch, save_api_url)
            chat = make_chat(f'user {self.current_user},url({url}) is processing.')
            chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', message=chat))
            self.write_message(chat)
        else:
            chat = make_chat(f"[{self.current_user}]:{parese['body']}")
            chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', message=chat))
            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_updates(chat)
