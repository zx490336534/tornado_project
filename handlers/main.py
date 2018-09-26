import tornado.web
from pycket.session import SessionMixin
from utils.photo import get_images,ImageSave
from utils.account import add_post, get_post_for, get_post


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user_info')


class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds of follow.
    """

    @tornado.web.authenticated  # self.current_user 非None
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        self.render('index.html', posts=posts)


class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = get_post_for(self.current_user)
        self.render('explore.html', posts=posts)


class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page,and maybe comments.
    """
    def get(self, post_id):
        posts = get_post(post_id)
        if not posts:
            self.write('post id not exists')
        else:
            self.render('post.html', posts=posts)


class UploadFileHandler(AuthBaseHandler):
    """
    处理上传的图片文件，保存到硬盘
    """
    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        self.render('upload.html')

    @tornado.web.authenticated
    def post(self, *args, **kwargs):
        img_files = self.request.files.get('newimg', None)
        for img in img_files:
            img_saver = ImageSave(self.settings['static_path'],img['filename'])
            img_saver.save_upload(img['body'])
            img_saver.make_thumb()

            add_post(self.current_user, img_saver.upload_url, img_saver.thumb_url)
        self.write('upload done')
