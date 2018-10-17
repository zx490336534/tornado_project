# coding=utf-8
# Auth:zx
# Time:2018/10/14 0014 10:20
import uuid
from datetime import datetime
import tornado.httpclient
import tornado.web
import tornado.gen
import tornado.escape
from .main import AuthBaseHandler
from .chat import ChatSocketHandler,make_chat
from utils.photo import ImageSave
from utils.account import add_post


class AsyncURLSaveHandler(AuthBaseHandler):
    """
    实现保存指定URL的图片功能.异步版本
    """

    # @tornado.web.authenticated
    @tornado.gen.coroutine
    def get(self, *args, **kwargs):
        resp = yield self.fetch_image()

        if not resp.body:
            self.write('empty data')
            return

        img_saver = ImageSave(self.settings['static_path'], 'x.jpg')
        img_saver.save_upload(resp.body)
        img_saver.make_thumb()
        user = self.get_argument('user','')
        is_from_room = self.get_argument('room','') == 'room'
        if user and is_from_room:
            post = add_post(user, img_saver.upload_url, img_saver.thumb_url)
            print(f'--  {datetime.now()} -end fetch:#{post.id}')
            chat = make_chat(f'-----[{user}]-----',img_saver.thumb_url)
            chat['post_id'] = post.id
            chat['html'] = tornado.escape.to_basestring(self.render_string('message.html', message=chat))
            ChatSocketHandler.update_cache(chat)
            ChatSocketHandler.send_updates(chat)
        else:
            self.write('user error')
        # self.redirect('/post/{}'.format(post.id))

    @tornado.gen.coroutine
    def fetch_image(self):
        url = self.get_argument('url', '')
        client = tornado.httpclient.AsyncHTTPClient()
        print(f'-- {datetime.now()} -going to fetch:{url}')
        # yield tornado.gen.sleep(5)
        resp = yield client.fetch(url)
        return resp


class URLSaveHandler(AuthBaseHandler):
    """
    实现保存指定URL的图片功能.同步版本
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        url = self.get_argument('url', '')
        client = tornado.httpclient.HTTPClient()
        try:
            resp = client.fetch(url)
            img_saver = ImageSave(self.settings['static_path'], 'x.jpg')
            img_saver.save_upload(resp.body)
            img_saver.make_thumb()
            post = add_post(self.current_user, img_saver.upload_url, img_saver.thumb_url)
            self.redirect('/post/{}'.format(post.id))
        except tornado.httpclient.HTTPError as e:
            print("Error: " + str(e))
        except Exception as e:
            print("Error: " + str(e))
        client.close()

