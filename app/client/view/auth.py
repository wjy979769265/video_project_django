# coding:utf-8


from django.views.generic import View

from app.libs.base_render import render_to_response
from app.model.auth import ClientUser
from app.utils.permission import dashboard_auth, client_auth
from django.shortcuts import redirect, reverse
from django.http import JsonResponse
from app.utils.permission import client_auth
from app.utils.consts import COOKIE_NAME
import datetime


class User(View):
    TEMPLATE = 'client/auth/user.html'

    def get(self, request):

        # 验证一下是否有用户，如有则返回user
        user = client_auth(request)

        data = {
            'user': user
        }

        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段'
            return JsonResponse({
                'code': -1,
                'msg': error
            })
        user = ClientUser.get_user(username, password)
        if not user:
            error = '用户名或密码错误'
            return JsonResponse({
                'code': -1,
                'msg': error
            })
        # 设置一个cookie
        # 用cookie保持登陆状态，不设置时间，持久化登陆

        # 可以用datetime设置过期时间
        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, str(user.id))
        return response


class Regist(View):
    TEMPLATE = 'client/auth/user.html'

    def post(self, request):
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        if not all([username, password]):
            error = '缺少必要字段'
            return JsonResponse({
                'code': -1,
                'msg': error
            })
        exists = ClientUser.objects.filter(username=username).exists()
        if exists:
            error = '该用户已经存在'
            return JsonResponse({
                'code': -1,
                'msg': error
            })
        ClientUser.add(username=username, password=password)

        return JsonResponse({
            'code': 0,
            'msg': '注册成功'
        })


class Logout(View):
    TEMPLATE = 'client/auth/user.html'

    def get(self, request):
        response = render_to_response(request, self.TEMPLATE)
        response.set_cookie(COOKIE_NAME, '')

        return response
