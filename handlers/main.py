import tornado.web
from pycket.session import SessionMixin
from utils.photo import get_images, make_thumb


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user_info')


class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds of follow.
    """

    @tornado.web.authenticated  # self.current_user 非None
    def get(self, *args, **kwargs):
        names = get_images('uploads')
        self.render('index.html', imgs=names)


class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        names = get_images('uploads/thumbs')
        self.render('explore.html', imgs=names)


class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page, and maybe comments.
    """

    def get(self, post_id):
        self.render('post.html', post_id=post_id)


class UploadFileHandler(tornado.web.RequestHandler):
    """
    处理上传的图片文件，保存到硬盘
    """

    def get(self, *args, **kwargs):
        self.render('upload.html')

    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg', None)
        for img in img_files:
            save_to = './static/uploads/{}'.format(img['filename'])
            with open(save_to, 'wb') as f:
                f.write(img['body'])
            make_thumb(save_to)
        self.write('upload done')
