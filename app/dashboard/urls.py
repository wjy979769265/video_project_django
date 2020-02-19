# coding:utf-8


from django.urls import path

from .views.base import Index
from .views.auth import Login, AdminManager, Logout, UpdateAdminStatus
from .views.video import *

urlpatterns = [
    path('', Index.as_view(), name='dashboard_index'),
    path('login', Login.as_view(), name='login'),
    path('admin/manager', AdminManager.as_view(), name='admin_manager'),
    path('logout', Logout.as_view(), name='logout'),
    path('admin/manager/update/status', UpdateAdminStatus.as_view(), name='admin_update_status'),
    path('video/external_video', ExternalVideo.as_view(), name='external_video'),
    path('video/videoSub/<int:video_id>', VideoSubPage.as_view(), name='video_sub'),
    path('video/star', VideoStarView.as_view(), name='video_star'),
    path('video/star/delete/<int:star_id>/<int:video_id>', StarDeleter.as_view(), name='delete_star'),
    path('video/star/update/<int:video_id>', VideoUpdate.as_view(), name='video_update'),
]
