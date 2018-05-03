# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/10 15:20'

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

'''
在用户点击开始学习是，判断用户是否已经登录， 
login_required 判断了用户是否已登录，没有登录 跳转到登录界面
'''


class LoginRequiredMixin(object):

    @method_decorator(login_required(login_url='/users/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin,self).dispatch(request,*args,**kwargs)