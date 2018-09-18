# coding=utf-8
# Auth:zx
# Time:2018/9/18 0018 22:13
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


def make_thumb(path):
    '''
    为指定的 path 文件生成它所在的目录的thumbs目录的小图文件
    :param path:
    :return:
    '''
    im = Image.open(path)
    size = (200, 200)
    im.thumbnail(size)
    dirname = os.path.dirname(path)
    filename = os.path.basename(path)
    file, ext = os.path.splitext(filename)
    save_thumb_to = os.path.join(dirname, 'thumbs', '{}_{}x{}{}'.format(file, *size, ext))
    im.save(save_thumb_to, 'JPEG')
    return save_thumb_to
