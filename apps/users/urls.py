# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/12 12:54'

from django.urls import path,include

from users.views import LoginView,LogoutView,RegisterView,ActiveUserView,ForgetPwdView,ResetView,ModifyPwdView
from users.views import IndexView
from .views import UserInfoView,ImageUploadView,UserCenterModifyPwdView,SendEmailCodeView
from .views import UpdateEmailView,UserCoursesView,MyFavOrgView,MyFavCourseView,MyFavTeacherView,MyMessageView

app_name='users'

urlpatterns = [
    # path('', IndexView.as_view(), name='index'),  # as_view方法将Template转换成view
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('active/<active_code>', ActiveUserView.as_view(), name='user_active'),
    path('forget/', ForgetPwdView.as_view(), name='forget_pwd'),
    path('reset/<active_code>', ResetView.as_view(), name='reset_pwd'),
    path('Modify_pwd/', ModifyPwdView.as_view(), name='modify_pwd'),

    # 用户个人信息
    path('info/', UserInfoView.as_view(), name='user_info'),

    # 用户头像上传
    path('image/upload/', ImageUploadView.as_view(), name='image_upload'),
    # 用户个人中心修改密码
    path('update/pwd', UserCenterModifyPwdView.as_view(), name='update_pwd'),
    #发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),
    #修改邮箱
    path('update_email/', UpdateEmailView.as_view(), name='update_email'),


    #用户课程
    path('user_courses/', UserCoursesView.as_view(), name='user_courses'),
    #用户课程机构收藏
    path('myfav/org/', MyFavOrgView.as_view(), name='myfav_org'),
    # 用户讲师收藏
    path('myfav/teacher/', MyFavTeacherView.as_view(), name='myfav_teacher'),
    #用户课程收藏
    path('myfav/course/', MyFavCourseView.as_view(), name='myfav_course'),
    # 我的消息
    path('mymessage/', MyMessageView.as_view(), name='mymessage'),

]