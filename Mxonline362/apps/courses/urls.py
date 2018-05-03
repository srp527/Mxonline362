# -*- coding:utf-8 -*- 
__author__ = 'SRP'

from django.urls import path,include

from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentsView,VideoPlayView
app_name='course'
urlpatterns = [
    # 课程列表页
    path('list/', CourseListView.as_view(), name='course_list'),

    #课程详情页
    path('detail/<course_id>', CourseDetailView.as_view(), name='course_detail'),

    #课程章节信息页
    path('info/<course_id>', CourseInfoView.as_view(), name='course_info'),

    #课程评论页
    path('comment/<course_id>', CourseCommentView.as_view(), name='course_comment'),

    #添加课程评论
    path('add_comment/',AddCommentsView.as_view(),name='add_comment'),

    #视频播放页
    path('video/<video_id>',VideoPlayView.as_view(),name='video_play'),
]

