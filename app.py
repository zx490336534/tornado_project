import tornado.ioloop
import tornado.options
import tornado.web
from tornado.options import define, options

from handlers import main, auth, chat

define('port', default='8000', help='Listening port', type=int)


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            ('/', main.IndexHandler),
            ('/explore', main.ExploreHandler),
            ('/post/(?P<post_id>[0-9]+)', main.PostHandler),
            ('/upload', main.UploadFileHandler),
            ('/profile', main.ProfileHander),
            ('/login', auth.LoginHandler),
            ('/loginout', auth.LogoutHandler),
            ('/signup', auth.SignupHandler),
            ('/room', chat.RoomHanlder),
            ('/ws', chat.ChatSocketHandler),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            login_url='/login',
            cookie_secret='sdjfalkfjlaj148039815',
            pycket={
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    'port': 6379,
                    'db_sessions': 5,  # select 5
                    'db_notifications': 11,
                    'max_connections': 2 ** 30,
                },
                'cookies': {
                    'expires_days': 30,
                }
            }
        )

        super(Application, self).__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    application.listen(options.port)
    print("Server start on port {}".format(str(options.port)))
    tornado.ioloop.IOLoop.current().start()
