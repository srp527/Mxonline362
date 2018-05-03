# -*- coding:utf-8 -*-
import json

from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q

from.models import Course,CourseResource,Video
from operation.models import UserFavorite,CourseComments,UserCourse
from utils.mixin_utils import LoginRequiredMixin

class CourseListView(View):
    '''
    课程列表页
    '''
    def get(self, request):
        #默认按照添加时间排序  最新-->最早
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]

        #课程搜索
        search_keywords = request.GET.get('keywords','')
        if search_keywords: #__icontains可以做like语句操作 i不区分大小写
            all_courses = all_courses.filter(Q(name__icontains=search_keywords)|
                                             Q(desc__icontains=search_keywords)|
                                             Q(detail__icontains=search_keywords))


        #按照 热度或学习人数排序
        sort = request.GET.get('sort','')
        if sort == 'hot':
            all_courses = all_courses.order_by('-click_nums')
        elif sort == 'students':
            all_courses = all_courses.order_by('-students')

        # 对课程进行分页显示
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, 3, request=request)  # 3 第二个参数表示每页显示的个数
        courses = p.page(page)

        return render(request,'course-list.html',{
            'all_courses':courses,
            'sort':sort,
            'hot_courses':hot_courses,
        })


class CourseDetailView(View):
    '''
    课程详情页
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1  #增加课程点击数
        course.save()

        tag = course.tag
        if tag:
            relate_courses = Course.objects.filter(tag=tag)[:2]
        else:
            relate_courses = [ ]  #没有tag的话就传一个空数组

        # 判断用户是否已收藏该课程或课程机构
        has_fav_course = False
        has_fav_course_org = False
        fav_id_course = course.id
        fav_id_course_org = course.course_org.id
        if request.user.is_authenticated == True :
            if UserFavorite.objects.filter(user=request.user, fav_id=fav_id_course, fav_type=1):
                has_fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=fav_id_course_org, fav_type=2):
                has_fav_course_org = True
        return render(request,'course-detail.html',{
            'course':course,
            'relate_courses':relate_courses,
            'has_fav_course':has_fav_course,
            'has_fav_course_org':has_fav_course_org,
        })


class CourseInfoView(LoginRequiredMixin,View):
    '''
    课程章节信息页
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))
        course.students += 1
        course.save()

        #查询用户是否已经关联了该课程,没有就创建一个关联
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses ]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)#user_id__in django自带的传入的是个list

        course_ids = [user_course.course.id for user_course in all_user_courses]#取出所有课程ID
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5] #取出学过该课程的其他用户学过的所有课程前五个

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-video.html', {
            'course': course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
        })


class CourseCommentView(LoginRequiredMixin,View):
    '''
    课程评论页
    '''
    def get(self,request,course_id):
        course = Course.objects.get(id=int(course_id))

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)  # user_id__in django自带的传入的是个list

        course_ids = [user_course.course.id for user_course in all_user_courses]  # 取出所有课程ID
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5]  # 取出学过该课程的其他用户学过的所有课程前五个

        all_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request,'course-comment.html',{
            'course':course,
            'all_resources': all_resources,
            'all_comments':all_comments,
            'relate_courses': relate_courses,

        })


class AddCommentsView(View):
    '''
    用户添加课程评论
    '''
    def post(self,request):
        #先判断用户是否登录
        if not request.user.is_authenticated:
            f = {'static':'fail','msg':'用户未登录'}
            return HttpResponse(json.dumps(f),content_type='application/json')
        course_id = request.POST.get('course_id',0)
        comments = request.POST.get('comments','')
        if course_id > 0 and comments:
            course_comments = CourseComments()
            course = Course.objects.get(id=int(course_id))
            course_comments.user = request.user
            course_comments.course = course
            course_comments.comments = comments
            course_comments.save()
            f = {'status': 'success', 'msg': '添加成功'}
            return HttpResponse(json.dumps(f), content_type='application/json')
        else:
            f = {'status': 'fail', 'msg': '添加失败'}
            return HttpResponse(json.dumps(f), content_type='application/json')


class VideoPlayView(View):
    '''
    视频播放页面
    '''
    def get(self,request,video_id):
        video = Video.objects.get(id=int(video_id))
        course = video.lesson.course

        #查询用户是否已经关联了该课程,没有就创建一个关联
        user_courses = UserCourse.objects.filter(user=request.user,course=course)
        if not user_courses:
            user_course = UserCourse(user=request.user,course=course)
            user_course.save()

        user_courses = UserCourse.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses ]
        all_user_courses = UserCourse.objects.filter(user_id__in=user_ids)#user_id__in django自带的传入的是个list

        course_ids = [user_course.course.id for user_course in all_user_courses]#取出所有课程ID
        relate_courses = Course.objects.filter(id__in=course_ids).order_by('-click_nums')[:5] #取出学过该课程的其他用户学过的所有课程前五个

        all_resources = CourseResource.objects.filter(course=course)

        return render(request, 'course-play.html', {
            'course': course,
            'all_resources':all_resources,
            'relate_courses':relate_courses,
            'video':video

        })




