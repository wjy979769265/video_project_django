# coding:utf-8

from django.views.generic import View
from django.shortcuts import redirect, reverse, get_object_or_404
from app.libs.base_render import render_to_response
from app.model.video import Video, FromType, VideoSub
from app.utils.permission import dashboard_auth


class ExVideo(View):
    TEMPLATE = 'client/video.html'

    def get(self, request):
        videos = Video.objects.exclude(from_to=FromType.custom.value)

        data = {
            'videos': videos
        }

        return render_to_response(request, self.TEMPLATE, data)


class CusVideo(View):
    TEMPLATE = 'client/video.html'

    def get(self, request):
        videos = Video.objects.filter(from_to=FromType.custom.value)

        data = {
            'videos': videos
        }

        return render_to_response(request, self.TEMPLATE, data)


class VideoSubDetail(View):
    TEMPLATE = 'client/video_sub.html'

    def get(self, request, video_id):
        video = get_object_or_404(Video, pk=video_id)

        data = {
            'video': video
        }

        # print('videoSubs')
        # print(videoSubs)

        return render_to_response(request, self.TEMPLATE, data)
