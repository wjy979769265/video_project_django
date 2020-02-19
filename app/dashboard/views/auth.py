# coding:utf-8
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import *
from django.urls import reverse
from django.views.generic import View
from django.shortcuts import redirect
from django.core.paginator import Paginator
from app.utils.permission import dashboard_auth

from app.libs.base_render import render_to_response


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class Login(View):
    TEMPLATE = 'dashboard/auth/login.html'

    def get(self, request):
        to = request.GET.get('to', '')
        data = {
            'error': '',
            'to': to
        }
        if request.user.is_authenticated:
            return redirect(reverse('dashboard_index'))
        return render_to_response(request, self.TEMPLATE, data)

    def post(self, request):
        to_page = request.GET.get('to')
        username = request.POST.get('username')
        password = request.POST.get('password')
        print('username' + username + password)
        data = {'error': ''}
        exists = User.objects.filter(username=username).exists()

        if not exists:
            data['error'] = '不存在该用户'
            return render_to_response(request, self.TEMPLATE, data)
        user = authenticate(username=username, password=password)
        if not user:
            data['error'] = '密码错误'
            return render_to_response(request, self.TEMPLATE, data)
        if not user.is_superuser:
            data['error'] = '你无权登陆'
            return render_to_response(request, self.TEMPLATE, data)
        login(request, user)

        if to_page:
            return redirect(to_page)
        return redirect(reverse('dashboard_index'))


class AdminManager(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    @dashboard_auth
    def get(self, request):
        users = User.objects.all()
        # 分页
        page = request.GET.get('page', 1)
        p = Paginator(users, 2)

        total_page = p.num_pages

        if int(page) <= 1:
            page = 1
        current_page = p.get_page(int(page)).object_list
        data = {
            'users': current_page,
            'current_page_objects': current_page,
            'total_page': int(total_page),
            'page_num': int(page)

        }
        print(current_page)

        return render_to_response(request, self.TEMPLATE, data)


class UpdateAdminStatus(View):
    TEMPLATE = 'dashboard/auth/admin.html'

    def get(self, request):
        status = request.GET.get('status', 'on')
        _status = True if status == 'on' else False
        print(status)
        print(_status)
        request.user.is_superuser = _status
        request.user.save()

        return redirect(reverse('admin_manager'))
