import tornado.web
from pycket.session import SessionMixin
from utils.photo import get_images, make_thumb
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
            image_url = 'uploads/{}'.format(img['filename'])
            save_to = './static/{}'.format(image_url)
            with open(save_to, 'wb') as f:
                f.write(img['body'])
            save_thumb_to = make_thumb(save_to)
            import os
            thumb_url = os.path.relpath(save_thumb_to, 'static')

            add_post(self.current_user, image_url, thumb_url)
        self.write('upload done')
