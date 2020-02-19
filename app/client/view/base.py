# coding:utf-8


from django.views.generic import View

from app.libs.base_render import render_to_response
from app.utils.permission import dashboard_auth
from django.shortcuts import redirect, reverse


class Index(View):
    TEMPLATE = 'client/base.html'

    # @dashboard_auth
    def get(self, request):

        return render_to_response(request,self.TEMPLATE)

        # return redirect(reverse('client_ex_video'))
