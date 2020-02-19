# coding:utf-8


from qiniu import Auth, put_data, put_file
from django.conf import settings


class Qiniu(object):
    def __init__(self, bucket_name, base_url):
        self.bucket_name = bucket_name
        self.base_url = base_url
        self.q = Auth(settings.QINIU_AK, settings.QINIU_SK)

    def put(self, name, path):
        token = self.q.upload_token(self.bucket_name, name)
        print('上传了这个路径的文件：' + path)
        print('在云储存的文件名是' + name)
        ret, info = put_file(token, name, path)

        if 'key' in ret:
            remote_url = '/'.join([self.base_url, ret['key']])

            return remote_url
        print('ret' + ret)
        print('info' + info)


video_qiniu = Qiniu(bucket_name=settings.QINIU_VIDEO, base_url=settings.QINIU_VIDEO_URL)
