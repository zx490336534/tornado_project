import tornado.web
from pycket.session import SessionMixin
from utils.photo import get_images, ImageSave
from utils.account import HandlerORM
from models.db import DBSession


class AuthBaseHandler(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('tudo_user_info')

    def prepare(self):
        self.db_session = DBSession()
        self.orm = HandlerORM(self.db_session, self.current_user)

    def on_finish(self):
        self.db_session.close()


class IndexHandler(AuthBaseHandler):
    """
    Home page for user, photo feeds of follow.
    """

    @tornado.web.authenticated  # self.current_user 非None
    def get(self, *args, **kwargs):
        posts = self.orm.get_post_for_user()
        self.render('index.html', posts=posts)


class ExploreHandler(AuthBaseHandler):
    """
    Explore page, photo of other users.
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        posts = self.orm.get_all_posts()  # 展示全部用户上传的图片
        self.render('explore.html', posts=posts)


class PostHandler(AuthBaseHandler):
    """
    Single photo page,and maybe comments.
    """

    def get(self, post_id):
        posts = self.orm.get_post(post_id)
        if not posts:
            self.write('post id not exists')
        else:
            like_count = self.orm.get_like_count(posts)
            self.render('post.html', posts=posts, like_count=like_count)


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
        post_id = 0
        for img in img_files:
            img_saver = ImageSave(self.settings['static_path'], img['filename'])
            img_saver.save_upload(img['body'])
            img_saver.make_thumb()

            post = self.orm.add_post_for_user(img_saver.upload_url, img_saver.thumb_url)
            post_id = post.id
        self.redirect('/post/{}'.format(post_id))


class ProfileHander(AuthBaseHandler):
    """
    显示用户上传的图片和喜欢的图片列表
    """

    @tornado.web.authenticated
    def get(self, *args, **kwargs):
        username = self.get_argument('name', None)
        if not username:
            username = self.current_user
        self.orm.username = username
        user = self.orm.get_user()
        like_posts = self.orm.get_like_posts(user)
        self.render('profile.html', user=user, like_posts=like_posts)
