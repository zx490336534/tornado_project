# coding=utf-8
# Auth:zx
# Time:2018/10/9 0009 21:25
import uuid

import tornado.web
import tornado.websocket
from .main import AuthBaseHandler
import tornado.escape


class RoomHanlder(AuthBaseHandler):
    """
    聊天室页面
    """

    def get(self, *args, **kwargs):
        self.render('room.html',messages=ChatSocketHandler.cache)


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    """
    处理响应 websocker 连接
    """
    waiters = set()     #等待接收信息的用户
    cache = []          #存放消息
    cache_size = 200    #消息列表的大小

    def open(self, *args, **kwargs):
        """新的WebSocket连接打开，自动调用"""
        print('new connetcon :%s' % self)
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """WebSocket连接断开，自动调用"""
        print('close connetcion: %s' % self)
        ChatSocketHandler.waiters.remove(self)

    @classmethod
    def update_cache(cls,chat):
        """更新消息列表，加入新的消息"""
        cls.cache.append(chat)
        if len(cls.cache) > cls.cache_size:
            cls.cache = cls.cache[-cls.cache_size:]

    @classmethod
    def send_updates(cls,chat):
        """给每个等待接收的用户发送新的消息"""
        for waiter in cls.waiters:
            waiter.write_message(chat)

    def on_message(self, message):
        """WebSocket 服务端接收到消息，自动调用"""
        print('got message :%s' % message)
        parese = tornado.escape.json_decode(message)
        chat = {
            'id':str(uuid.uuid4()),
            'body':parese['body'],
        }
        chat['html'] = tornado.escape.to_basestring(self.render_string('message.html',message=chat))
        ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
