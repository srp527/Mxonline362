# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from .models import CourseOrg,CityDict,Teacher
from .forms import UserAskForm
from courses.models import Course
from operation.models import UserFavorite
# Create your views here.


class OrgView(View):
    '''
    课程机构列表功能
    '''
    def get(self,request):
        #课程机构/城市
        # current_page = 'org'
        all_orgs = CourseOrg.objects.all()
        hot_orgs = all_orgs.order_by('-click_num')[:3]
        all_citys = CityDict.objects.all()
        # all_courses = course_org.course_set.all()[:3]

        # 机构搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:  # __icontains可以做like语句操作 i不区分大小写
            all_orgs = all_orgs.filter(Q(name__icontains=search_keywords)|
                                       Q(desc__icontains=search_keywords))

        #取出筛选城市
        city_id = request.GET.get('city','')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        #类别筛选
        category = request.GET.get('ct','')
        if category:
            all_orgs = all_orgs.filter(category=category)

        sort = request.GET.get('sort','') #根据学习人数或课程数排序
        if sort:
            if sort == 'students':
                all_orgs = all_orgs.order_by('-students')
            elif sort == 'courses':
                all_orgs = all_orgs.order_by('-course_nums')

        org_nums = all_orgs.count()
        #对课程机构进行分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_orgs, 2,request=request) #5每页显示的个数
        orgs = p.page(page)

        return render(request,'org-list.html',{
            'all_orgs':orgs,
            'all_citys':all_citys,
            'org_nums':org_nums,
            'city_id':city_id,
            'category':category,
            'hot_orgs':hot_orgs,
            'sort':sort,
            # 'current_page':current_page,
        })


class AddUserAskView(View):
    '''
    用户添加咨询
    '''
    def post(self,request): #因为form继承自ModelForm，所以可以直接用Model的save（）方法
        userask_form = UserAskForm(request.POST)
        if userask_form.is_valid():
            user_ask = userask_form.save(commit=True)#ModelForm的方便之处
            name_dict = {'status':'success',}
            return HttpResponse(json.dumps(name_dict), content_type='application/json')
        else:
            name_dict = {'status':'fail','msg':'添加出错!'}
            return HttpResponse(json.dumps(name_dict),content_type='application/json')


class OrgHomeView(View):
    '''
    机构首页
    '''
    def get(self,request,org_id):
        current_page = 'home'
        course_org = CourseOrg.objects.get(id=int(org_id))
        course_org.click_num += 1
        course_org.save()
        #判断用户是否已收藏改课程机构
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user,fav_id=course_org.id,fav_type=2):
                has_fav = True

        #Django:凡是有外键的地方都可以通过xxx_set反向取出关联的数据
        all_courses = course_org.course_set.all()[:3]
        all_teachers = course_org.teacher_set.all()[:3]
        return render(request,'org-detail-homepage.html',{
            'all_courses':all_courses,
            'all_teachers':all_teachers,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav':has_fav,
        })


class OrgCourseView(View):
    '''
    机构课程列表页
    '''
    def get(self,request,org_id):
        current_page = 'course'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否已收藏改课程
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        #Django:凡是有外键的地方都可以通过xxx_set反向取出关联的数据
        all_courses = course_org.course_set.all()
        return render(request,'org-detail-course.html',{
            'all_courses':all_courses,
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


class OrgDescView(View):
    '''
    机构介绍页
    '''
    def get(self,request,org_id):
        current_page = 'desc'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否已收藏改课程
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True
        return render(request,'org-detail-desc.html',{
            'course_org':course_org,
            'current_page':current_page,
            'has_fav': has_fav,
        })


class OrgTeacherView(View):
    '''
    机构讲师页
    '''
    def get(self,request,org_id):
        # current_page = 'teacher'
        course_org = CourseOrg.objects.get(id=int(org_id))
        # 判断用户是否已收藏改课程
        has_fav = False
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=course_org.id, fav_type=2):
                has_fav = True

        all_teachers = course_org.teacher_set.all()


        return render(request,'org-detail-teachers.html',{
            'all_teachers':all_teachers,
            'course_org':course_org,
            # 'current_page':current_page,
            'has_fav': has_fav,
        })


class AddFavView(View):
    '''
    用户收藏或取消收藏
    '''
    def post(self,request):
        fav_id = request.POST.get('fav_id',0)
        fav_type = request.POST.get('fav_type',0)

        if not request.user.is_authenticated:
        #判断用户登录状态
            f = {'status':'fail','msg':'用户未登录'}
            return HttpResponse(json.dumps(f),content_type='application/json')
        exist_records = UserFavorite.objects.filter(user=request.user,fav_id=int(fav_id),fav_type=int(fav_type))
        if exist_records:
            #如果记录已经存在，则表示用户取消收藏
            exist_records.delete()

            if int(fav_type) == 1:
                course = Course.objects.get(id=int(fav_id))
                course.fav_nums -= 1
                if course.fav_nums < 0:
                    course.fav_nums = 0
                course.save()
            if int(fav_type) == 2:
                courseorg = CourseOrg.objects.get(id=int(fav_id))
                courseorg.fav_nums -= 1
                if courseorg.fav_nums < 0:
                    courseorg.fav_nums = 0
                courseorg.save()
            if int(fav_type) == 3:
                teacher = Teacher.objects.get(id=int(fav_id))
                teacher.fav_nums -= 1
                if teacher.fav_nums < 0:
                    teacher.fav_nums = 0
                teacher.save()

            f = {'status': 'success', 'msg': '收藏'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            user_fav = UserFavorite()
            if int(fav_id) > 0 and int(fav_type) > 0:
                user_fav.user = request.user
                user_fav.fav_id = int(fav_id)
                user_fav.fav_type = int(fav_type)
                user_fav.save()

                if int(fav_type) == 1:
                    course = Course.objects.get(id=int(fav_id))
                    course.fav_nums += 1
                    course.save()
                if int(fav_type) == 2:
                    courseorg = CourseOrg.objects.get(id=int(fav_id))
                    courseorg.fav_nums += 1
                    courseorg.save()
                if int(fav_type) == 3:
                    teacher = Teacher.objects.get(id=int(fav_id))
                    teacher.fav_nums += 1
                    teacher.save()

                f = {'status': 'success', 'msg': '已收藏'}
                return HttpResponse(json.dumps(f), content_type='application/json')
            else:
                f = {'status': 'fail', 'msg': '收藏失败'}
                return HttpResponse(json.dumps(f), content_type='application/json')


class TeacherListView(View):
    '''
    课程讲师列表页
    '''
    def get(self,request):
        all_teachers = Teacher.objects.all()
        hot_teachers = all_teachers.order_by('-click_nums')[:3]

        # 讲师搜索
        search_keywords = request.GET.get('keywords', '')
        if search_keywords:  # __icontains可以做like语句操作 i不区分大小写
            all_teachers = all_teachers.filter(Q(name__icontains=search_keywords) |
                                               Q(work_company__icontains=search_keywords) |
                                               Q(work_position__icontains=search_keywords))

        sort = request.GET.get('sort', '')  # 根据学习人气（点击数）排序
        if sort:
            if sort == 'hot':
                all_teachers = all_teachers.order_by('-click_nums')

        teacher_nums = all_teachers.count()

        try:     # 对课程机构进行分页显示
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_teachers, 4, request=request)  # 5每页显示的个数
        teachers = p.page(page)

        return render(request,'teachers-list.html',{
            'teachers':teachers,
            'hot_teachers':hot_teachers,
            'teacher_nums':teacher_nums,
            'sort':sort,
        })


class TeacherDetailView(View):
    '''
    课程讲师详情页
    '''
    def get(self,request,teacher_id):
        teacher = Teacher.objects.get(id=int(teacher_id))
        teacher.click_nums += 1
        teacher.save()

        courses = Course.objects.filter(teacher=teacher)
        hot_teachers =  Teacher.objects.all().order_by('-click_nums')[:3]

        # 判断用户是否已收藏该讲师或 讲师所属机构
        has_fav_teacher = False
        has_fav_teacher_org = False
        # fav_id_teacher = teacher.id
        # fav_id_teacher_org = teacher.org.id
        fav_id_teacher = teacher.id
        fav_id_teacher_org = teacher.org.id
        if request.user.is_authenticated:
            if UserFavorite.objects.filter(user=request.user, fav_id=fav_id_teacher, fav_type=3):
                has_fav_teacher = True
            if UserFavorite.objects.filter(user=request.user, fav_id=fav_id_teacher_org, fav_type=2):
                has_fav_teacher_org = True

        return render(request,'teacher-detail.html',{
            'teacher':teacher,
            'courses':courses,
            'hot_teachers':hot_teachers,
            'has_fav_teacher':has_fav_teacher,
            'has_fav_teacher_org':has_fav_teacher_org,
        })


