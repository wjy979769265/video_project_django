# coding:utf-8


from django.urls import path

from app.client.view.auth import User, Regist, Logout
from app.client.view.base import Index
from app.client.view.video import ExVideo, VideoSubDetail, CusVideo

urlpatterns = [
    path('', Index.as_view(), name='client_index'),
    path('auth', User.as_view(), name='client_auth'),
    path('auth/regist', Regist.as_view(), name='client_auth_regist'),
    path('auth/logout', Logout.as_view(), name='client_auth_logout'),
    path('video/cus', CusVideo.as_view(), name='client_cus_video'),
    path('video/ex', ExVideo.as_view(), name='client_ex_video'),
    path('video/cus', CusVideo.as_view(), name='client_cus_video'),
    path('video/<int:video_id>', VideoSubDetail.as_view(), name='client_video_sub')

]
