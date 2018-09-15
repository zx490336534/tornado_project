import tornado.web


class IndexHandler(tornado.web.RequestHandler):
    """
    Home page for user, photo feeds of follow.
    """
    def get(self, *args, **kwargs):
        self.render('index.html')


class ExploreHandler(tornado.web.RequestHandler):
    """
    Explore page, photo of other users.
    """
    def get(self, *args, **kwargs):
        self.render('explore.html')


class PostHandler(tornado.web.RequestHandler):
    """
    Single photo page, and maybe comments.
    """
    def get(self, post_id):
        self.render('post.html', post_id=post_id)