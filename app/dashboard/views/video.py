# coding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import redirect
from django.core.paginator import Paginator
from app.utils.permission import dashboard_auth
from app.utils.common import check_and_get_video_type, handle_video
from app.libs.base_render import render_to_response
from app.model.auth import ClientUser
from app.model.video import NationlityType, Video, VideoStar, VideoSub, VideoType, FromType, IdentityType


class ExternalVideo(View):
    TEMPLATE = '/dashboard/video/external_video.html'

    @dashboard_auth
    def get(self, request):

        error = request.GET.get('error')
        data = {
            'error': error
        }

        ex_videos = Video.objects.exclude(from_to=FromType.custom.value)
        cus_video = Video.objects.filter(from_to=FromType.custom.value)
        data['ex_videos'] = ex_videos
        data['cus_videos'] = cus_video
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        name = request.POST.get('name')
        image = request.POST.get('image')
        video_type = request.POST.get('video_type')
        from_to = request.POST.get('from_to')
        nationality = request.POST.get('nationality')
        info = request.POST.get('info')
        video_id = request.POST.get('video_id')

        if video_id:
            reverse_path = reverse('video_update', kwargs={
                'video_id': video_id
            })

        if not all([name, image, video_type, from_to, nationality]):
            return redirect('{}?error={}'.format(reverse('external_video'), '缺少必要字段'))

        result = check_and_get_video_type(VideoType, video_type, '非法的视频类型')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result.get('msg')))
        video_type_obj = result.get('data')
        result = check_and_get_video_type(FromType, from_to, '非法的来源')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result.get('msg')))
        from_to_obj = result.get('data')
        result = check_and_get_video_type(NationlityType, nationality, '非法国家来源')
        if result.get('code') != 0:
            return redirect('{}?error={}'.format(reverse('external_video'), result.get('msg')))
        nationality_obj = result.get('data')
        if not video_id:
            try:
                Video.objects.create(
                    name=name,
                    image=image,
                    video_type=video_type_obj.value,
                    from_to=from_to_obj.value,
                    nationality=nationality_obj.value,
                    info=info
                )
            except:
                return redirect('{}?error={}'.format(reverse('external_video'), '创建失败'))
            # ${VideoType(video.video_type).label}
            return redirect(reverse('external_video'))
        else:
            try:
                print(name, image, video_type, from_to, nationality)
                video = Video.objects.get(pk=video_id)
                video.name = name
                video.image = image
                video.video_type = video_type
                video.from_to = from_to
                video.nationality = nationality
                video.save()
            except:
                return redirect('{}?error={}'.format(reverse_path, '修改失败'))
            return redirect(reverse('external_video'))


class VideoSubPage(View):
    TEMPLATE = '/dashboard/video/video_sub.html'

    @dashboard_auth
    def get(self, request, video_id):
        error = request.GET.get('error', '')
        video = Video.objects.get(pk=video_id)
        data = {
            'video': video,
            'error': error
        }
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        if FromType(video.from_to) == FromType.custom:
            url = request.FILES.get('url')
        else:
            url = request.POST.get('url')
        number = request.POST.get('number')
        print('url')
        print(url)
        if FromType(video.from_to) == FromType.custom:
            print('接收到了file')
            handle_video(url, video_id, number)
            return redirect(reverse('video_sub', kwargs={
                'video_id': video_id
            }))

        if not all([url, number]):
            return redirect(reverse('video_sub', kwargs={
                'video_id': video_id
            }) + '?error=缺少必要字段')
        try:
            VideoSub.objects.create(video=video, url=url, number=number)
        except:
            return redirect(reverse('video_sub', kwargs={
                'video_id': video_id
            }) + '?error=创建失败')
        print('add video sub success')
        return redirect(reverse('video_sub', kwargs={
            'video_id': video_id
        }))


class VideoStarView(View):

    def post(self, request):
        name = request.POST.get('name')
        identity = request.POST.get('identity')
        video_id = request.POST.get('video_id')

        if all([name, identity, video_id]):
            print()
            try:
                video = Video.objects.get(pk=video_id)
                VideoStar.objects.create(
                    video=video,
                    name=name,
                    identity=identity
                )
            except:
                return redirect(reverse('video_sub', kwargs={'video_id': video_id}) + '?error=创建失败')
        print(name, identity, video_id)
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class StarDeleter(View):
    def get(self, request, star_id, video_id):
        VideoStar.objects.filter(id=star_id).delete()
        # print(reverse('video_sub',kwargs={'video_id': video_id})+'/'+str(video_id))
        return redirect(reverse('video_sub', kwargs={'video_id': video_id}))


class VideoUpdate(View):
    TEMPLATE = '/dashboard/video/video_update.html'

    @dashboard_auth
    def get(self, request, video_id):
        video = Video.objects.get(pk=video_id)
        data = {
            'video': video
        }

        return render_to_response(request, self.TEMPLATE, data)
