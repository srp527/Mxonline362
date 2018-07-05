# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/7 18:42'

from django.urls import path,include

from .views import OrgView,AddUserAskView,OrgHomeView,OrgCourseView,OrgDescView,OrgTeacherView,AddFavView
from .views import TeacherListView,TeacherDetailView
app_name='org'
urlpatterns = [
    # 课程机构列表页
    path('list/', OrgView.as_view(), name='org_list'),
    path('add_ask/',AddUserAskView.as_view(),name='add_ask'),
    path('home/<org_id>',OrgHomeView.as_view(),name='org_home'),
    path('course/<org_id>',OrgCourseView.as_view(),name='org_course'),
    path('desc/<org_id>',OrgDescView.as_view(),name='org_desc'),
    path('org_teacher/<org_id>',OrgTeacherView.as_view(),name='org_teacher'),

    #机构收藏
    path('add_fav/',AddFavView.as_view(),name='add_fav'),
    #讲师列表页
    path('teacher/list/',TeacherListView.as_view(),name='teacher_list'),
    #讲师详情页
    path('teacher/detail/<teacher_id>',TeacherDetailView.as_view(),name='teacher_detail'),
    # # 讲师相关 urls 配置
    # path('teacher/', include('organization.urls', namespace='teacher')),

]
