from django.contrib import admin
from django.urls import path, include
from app.dashboard import urls as dashboard_urls
from app.client import urls as client_urls
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('dashboard/', include(dashboard_urls)),
    path('', include(client_urls)),
]

urlpatterns += staticfiles_urlpatterns()





