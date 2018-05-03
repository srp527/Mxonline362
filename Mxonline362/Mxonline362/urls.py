# -*- coding:utf-8 -*-
"""Mxonline path Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a path to urlpatterns:  path(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a path to urlpatterns:  path(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import path, include
    3. Add a path to urlpatterns:  path(r'^blog/', include(blog_urls))
"""
from django.urls import path,include,re_path
from django.contrib import admin
from django.views.generic import TemplateView
from django.views.static import serve #处理静态文件
import xadmin

from users.views import IndexView
from Mxonline362.settings import MEDIA_ROOT # ,STATIC_ROOT

urlpatterns = [
    path('xadmin/', xadmin.site.urls),

    path('', IndexView.as_view(), name='index'),  # as_view方法将Template转换成view
    #验证码
    path('captcha/',include('captcha.urls')),
    #课程机构urls 配置
    path('org/',include('organization.urls',namespace='org')),
    #课程相关 urls 配置
    path('course/',include('courses.urls',namespace='course')),

    #用户相关 urls 配置
    path('users/',include('users.urls',namespace='users')),

    #配置上传文件的访问处理函数
    # re_path('media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),
    re_path('media/(?P<path>.*)',serve,{'document_root':MEDIA_ROOT}),
    #配置静态文件的访问处理函数
#    re_path('static/(?P<path>.*)',serve,{'document_root':STATIC_ROOT}),

    #富文本相关
    path(r'ueditor/',include('DjangoUeditor.urls' )),


]
# + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#全局404页面
handler404 = 'users.views.page_not_found'
handler500 = 'users.views.page_error'
