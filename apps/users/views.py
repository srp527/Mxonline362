# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.backends import ModelBackend #这个类有authenticate方法
from django.contrib.auth.hashers import make_password #进行密码明文加密
from django.db.models import Q  #实现并集查询
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

from .models import UserProfile,EmailVerifyRecord,PageBanner
from .forms import LoginForm,RegisterForm,ForgetForm,ModifyPwdForm,UploadImageForm,UeerInfoForm
from utils.email_send import send_register_email
from utils.mixin_utils import LoginRequiredMixin
from operation.models import UserCourse,UserFavorite,UserMessage
from organization.models import CourseOrg
from courses.models import Course,Teacher


# Create your views here.

#自定义authenticate方法，实现可以用邮箱，用户名混合登录
#需要在settings.py中重载AUTHENTICATION_BACKENDS=( ,,)
class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username)|Q(email=username))
            #check_password方法 可以对password加密 并与数据库的作对比
            if user.check_password(password):
                return user
        except Exception as e:
            return None


#基于类来实现用户登录
class LoginView(View):
    #继承于View的函数 get post。Django会自动判断get、post方法而不用再使用if判断
    def get(self,request):
        return render(request, 'login.html', {})

    def post(self,request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get('username', '')
            pass_word = request.POST.get('password', '')
            # authenticate() Django向数据库验证用户密码是否正确  login才是登录
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                user1 = UserProfile.objects.get(Q(username=user_name) | Q(email=user_name))
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(reverse('index'))
                else:
                    return render(request, 'login.html', {'msg': '用户未激活'})
            else:
                return render(request, 'login.html', {'msg': '用户名或密码错误'})
        else:
            return render(request, 'login.html', {'login_form':login_form })


class LogoutView(View):
    '''
    用户退出
    '''
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('index')) #重定向


class ActiveUserView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
        else:
            return render(request, 'active_fail.html')
        return render(request,'login.html',{'email': email })


class RegisterView(View):

    def get(self,request):
        register_form = RegisterForm()
        return render(request, 'register.html',{'register_form': register_form })

    def post(self,request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_name = request.POST.get('email', '')
            pass_word = request.POST.get('password', '')
            user = UserProfile.objects.filter(Q(email=user_name)|Q(username=user_name))
            if user:
                return render(request,'register.html',{'register_form':register_form,'msg':'该邮箱已被注册'})
            else:
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.password = make_password(pass_word)
                user_profile.save()

                #写入欢迎注册消息
                user_message = UserMessage()
                user_message.user = user_profile.id
                user_message.message = '欢迎注册慕学在线网'
                user_message.save()

                send_register_email(user_name, 'register')
                return render(request, 'login.html', {'register_form': register_form})
        else:
            return render(request,'register.html',{'register_form':register_form })


class ForgetPwdView(View):
    '''找回密码'''
    def get(self,request):
        forget_form = ForgetForm()
        return render(request,'forgetpwd.html',{'forget_form':forget_form})

    def post(self,request):
        forget_form = ForgetForm(request.POST)
        if forget_form.is_valid():
            email = request.POST.get('email','')

            send_register_email(email,'forget') #发送重置密码的邮件
            return render(request,'send_success.html'.encode('utf8'))
        else:
            return render(request, 'forgetpwd.html'.encode('utf8'), {'forget_form': forget_form})


class ResetView(View):
    def get(self,request,active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                return render(request, 'password_reset.html'.encode('utf8'),{'email':email})
        else:
            return render(request, 'login.html')


class ModifyPwdView(View):
    '''
    修改用户密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2', '')
            email = request.POST.get('email','')
            if pwd1 != pwd2:
                return render(request, 'password_reset.html'.encode('utf8'), {'email': email,'msg':'密码不一致'})
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return render(request,'login.html',{'email':email})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html'.encode('utf8'), {'email': email,'modify_form':modify_form})


class UserInfoView(LoginRequiredMixin,View):
    '''
    用户个人信息
    '''
    def get(self,request):
        user = request.user
        return render(request,'usercenter-info.html'.encode('utf8'),{
            'user':user,
        })

    def post(self,request):
        user_info_form = UeerInfoForm(request.POST,instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            f = {'status': 'success'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')


class ImageUploadView(LoginRequiredMixin,View):
    '''
    用户头像上传
    '''
    def post(self,request):
        #instance传的是ModelForm指定的Model，也就是让image_from用上ModelForm的功能
        image_form = UploadImageForm(request.POST,request.FILES,instance=request.user)
        if image_form.is_valid():
            image_form.save()   #直接用Model的save（）保存
            f = {'status':'success'}
            return HttpResponse(json.dumps(f),content_type='application/json')
        else:
            f = {'status': 'fail'}
            return HttpResponse(json.dumps(f), content_type='application/json')


class UserCenterModifyPwdView(LoginRequiredMixin,View):
    '''
    个人中心修改用户密码
    '''
    def post(self,request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get('password1','')
            pwd2 = request.POST.get('password2', '')
            if pwd1 != pwd2:
                f = {'status': 'fail','msg':'密码不一致!请重新输入'}
                return HttpResponse(json.dumps(f),content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()
            f = {'status': 'success', 'msg': '密码修改成功'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type='application/json')


class SendEmailCodeView(LoginRequiredMixin,View):
    '''
    发送邮箱验证码
    '''
    def get(self,request):
        email = request.GET.get('email','')

        if UserProfile.objects.filter(email=email):
            f = {'email': '邮箱已被注册！'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        send_register_email(email,'update_email')
        f = {'status': 'success'}
        return HttpResponse(json.dumps(f), content_type='application/json')


class UpdateEmailView(LoginRequiredMixin,View):
    '''
    修改个人邮箱
    '''
    def post(self,request):
        email = request.POST.get('email','')
        code = request.POST.get('code','')

        existed_record = EmailVerifyRecord.objects.filter(email=email,code=code,send_type='update_email')
        if existed_record:
            user = request.user
            user.email = email
            user.save()
            f = {'status': 'success'}
            return HttpResponse(json.dumps(f), content_type='application/json')

        else:
            f = {'email': '验证码出错！'}
            return HttpResponse(json.dumps(f), content_type='application/json')


class UserCoursesView(LoginRequiredMixin,View):
    '''
    用户课程页
    '''
    def get(self,request):
        user_courses = UserCourse.objects.filter(user=request.user)
        return render(request,'usercenter-mycourse.html'.encode('utf8'),{'user_courses':user_courses })


class MyFavOrgView(LoginRequiredMixin,View):
    '''
    用户课程机构收藏页
    '''
    def get(self, request):
        org_list = []
        fav_orgs = UserFavorite.objects.filter(user=request.user,fav_type=2)
        for fav_org in fav_orgs:
            org_id = fav_org.fav_id
            org = CourseOrg.objects.get(id=org_id)
            org_list.append(org)
        return render(request, 'usercenter-fav-org.html'.encode('utf8'), {'org_list': org_list})


class MyFavTeacherView(LoginRequiredMixin,View):
    '''
    用户讲师收藏页
    '''
    def get(self, request):
        teacher_list = []
        fav_teachers = UserFavorite.objects.filter(user=request.user,fav_type=3)
        for fav_teacher in fav_teachers:
            org_id = fav_teacher.fav_id
            teacher = Teacher.objects.get(id=org_id)
            teacher_list.append(teacher)
        return render(request, 'usercenter-fav-teacher.html'.encode('utf8'), {'teacher_list': teacher_list})


class MyFavCourseView(LoginRequiredMixin,View):
    '''
    用户课程收藏页
    '''
    def get(self, request):
        course_list = []
        fav_courses = UserFavorite.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            course_id = fav_course.fav_id
            course = Course.objects.get(id=course_id)
            course_list.append(course)
        return render(request, 'usercenter-fav-course.html'.encode('utf8'), {'course_list': course_list})


class MyMessageView(LoginRequiredMixin,View):
    '''
    我的消息
    '''
    def get(self,request):
        #UserMessage中user存储的是user的id
        all_message = UserMessage.objects.filter(user=request.user.id)

        all_unread_messages = UserMessage.objects.filter(user=request.user.id,has_read=False)
        for message in all_unread_messages:
            message.has_read = True
            message.save()


        # 对课程机构进行分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_message, 2, request=request)  # 5每页显示的个数
        messages = p.page(page)

        return render(request,'usercenter-message.html'.encode('utf8'),{
            'messages':messages
        })


class IndexView(View):
    def get(self,request):
        # print 1/0
        #取出轮播图
        all_banners = PageBanner.objects.all().order_by('index')
        banner_courses = Course.objects.filter(is_banner=True)[:3]
        courses = Course.objects.filter(is_banner=False)[:6]
        course_orgs = CourseOrg.objects.all()[:15]
        return render(request,'index.html'.encode('utf8'),{
            'all_banners': all_banners,
            'banner_courses': banner_courses,
            'courses': courses,
            'course_orgs':course_orgs,

        })


# class LoginUnsafeView(View):
#     def get(self,request):
#         return render(request, 'login.html', {})
#     def post(self,request):
#         user_name = request.POST.get('username', '')
#         pass_word = request.POST.get('password', '')
#
#         import MySQLdb
#         conn = MySQLdb.connect(host= '192.168.30.11',
#                                user='root',
#                                password='1234',
#                                db='mxonline',
#                                charset='utf8',
#                                )
#         cursor = conn.cursor()
#         sql_select = "select * from users_userprofile where email='{0}' and password='{1}'".format(user_name,pass_word)
#         result = cursor.execute(sql_select)
#         for row in cursor.fetchall():
#             #查询到用户
#             pass


def page_not_found(request):
    #全局404处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('404.html',{ })
    response.status_code = 404
    return response


def page_error(request):
    #全局500处理函数
    from django.shortcuts import render_to_response
    response = render_to_response('500.html',{ })
    response.status_code = 500
    return response


#  # 基于函数的登录
# def user_login(request):
#     if request.method == 'POST':
#         user_name = request.POST.get('username','')
#         pass_word = request.POST.get('password','')
#         #authenticate Django向数据库验证用户密码是否正确  login才是登录
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#             user1 = UserProfile.objects.get(Q(username=user_name)|Q(email=user_name))
#             login(request,user)
#             return render(request,'index.html',{'user1':user1})
#         else:
#             return render(request,'login.html',{'msg':'用户名或密码错误' })
#     elif request.method == 'GET':
#         return render(request,'login.html',{ })

