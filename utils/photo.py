# coding=utf-8
# Auth:zx
# Time:2018/9/18 0018 22:13
import uuid

import os
import glob
from PIL import Image


def get_images(path):
    '''
    获取 static 目录下 path目录里面所有 .jpg结尾的文件
    :param path:
    :return:
    '''
    os.chdir('static')
    names = glob.glob('{}/*.jpg'.format(path))
    os.chdir('..')
    return names


class ImageSave(object):
    """
    辅助保存用户上传的图片，生成缩略图，保存图片相关URL用来存到数据库
    """
    upload_dir = 'uploads'
    thumb_dir = 'thumbs'
    size = (200, 200)

    def __init__(self, static_path, name):
        self.static_path = static_path
        self.old_name = name
        self.new_name = self.get_new_name()

    def get_new_name(self):
        """
        生成随机的唯一字符串的图片名
        :return:
        """
        _, ext = os.path.splitext(self.old_name)
        return uuid.uuid4().hex + ext

    @property
    def upload_url(self):
        return os.path.join(self.upload_dir,self.new_name)

    @property
    def upload_path(self):
        return os.path.join(self.static_path, self.upload_url)

    def save_upload(self, contenr):
        with open(self.upload_path, 'wb') as f:
            f.write(contenr)

    @property
    def thumb_url(self):
        filename, ext = os.path.splitext(self.new_name)
        thumb_name = '{}_{}x{}{}'.format(filename, *self.size, ext)
        return os.path.join(self.upload_dir, self.thumb_dir, thumb_name)

    def make_thumb(self):
        '''
        为指定的 path 文件生成它所在的目录的thumbs目录的小图文件
        :param path:
        :return:
        '''
        im = Image.open(self.upload_path)
        im.thumbnail(self.size)
        save_thumb_to = os.path.join(self.static_path, self.thumb_url)
        im.save(save_thumb_to, 'JPEG')
