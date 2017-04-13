# -*- encoding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
_author_ = 'shishengjia'
_date_ = '15/01/2017 16:14'


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='users/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(request, *args, **kwargs)