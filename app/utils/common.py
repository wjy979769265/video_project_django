# coding:utf-8
import os
import time

from django.conf import settings
import shutil

from app.model.video import Video, VideoSub
from app.tasks.task import video_task


def check_and_get_video_type(type_obj, type_value, message):
    try:
        final_type_obj = type_obj(type_value)
    except:
        return {
            'code': -1,
            'msg': message
        }
    return {
        'code': 0,
        'msg': 'success',
        'data': final_type_obj
    }


def remove_path(path):
    if os.path.exists(path):
        os.remove(path)


def handle_video(video_file, video_id, number):
    in_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_in')
    out_path = os.path.join(settings.BASE_DIR, 'app/dashboard/temp_out')
    name = '{}_{}'.format(int(time.time()), video_file.name)
    path_name = '/'.join([in_path, name])
    print('path', in_path)
    print('name', name)
    print('path_name', path_name)
    temp_path = video_file.temporary_file_path()
    shutil.copyfile(temp_path, path_name)
    out_name = '{}_{}'.format(int(time.time()), video_file.name.split('.')[0])
    print('out_name' + out_name)
    out_path = '/'.join([out_path, out_name])
    command = 'ffmpeg -i {} -c copy {}.mp4'.format(path_name, out_path)
    new_video_file_name = '.'.join([video_file.name.split('.')[0], 'mp4'])

    video = Video.objects.get(pk=video_id)
    video_sub = VideoSub.objects.create(
        video=video,
        url='',
        number=number
    )

    print('即将开始异步')

    result = video_task(command, out_path, path_name, new_video_file_name, number, video_sub.id)

    return result
