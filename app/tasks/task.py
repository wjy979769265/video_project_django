# coding:utf-8

import os
import time

from app.models import VideoSub, Video
from app.libs.base_qiniu import video_qiniu
from celery import task


@task
def video_task(command, out_path, path_name, video_file_name, number, video_sub_id):
    from app.utils.common import remove_path

    print('进入异步')
    print('开始转码')

    os.system(command)
    print('转码完成')

    out_name = '.'.join([out_path, 'mp4'])
    print('out_path'+out_path)
    print('out_name'+out_name)
    if not os.path.exists(out_name):
        return False
    print('111')

    final_name = '{}_{}'.format(int(time.time()), video_file_name)
    # 第一个为上传后保存的文件名 第二个为要上传的文件的本地路径
    url = video_qiniu.put(final_name, out_name)
    print('222')

    if url:
        try:
            videoSub = VideoSub.objects.get(pk=video_sub_id)
            videoSub.url = url
            videoSub.save()
            return True
        except:
            return False
        finally:
            remove_path(out_name)
            remove_path(path_name)
    remove_path(out_name)
    remove_path(path_name)
    return False
