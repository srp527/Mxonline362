# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/2 12:08'

import xadmin

from .models import Course,Lesson,Video,CourseResource,BannerCourse


class LessonInline(object):
    model = Lesson
    extra = 0


class CourseResourceInline(object):
    model = CourseResource
    extra = 0


class CourseAdmin(object):
    # 显示的列
    list_display = ['name', 'desc', 'detail', 'degree','learn_time','students','fav_nums','image','click_nums','add_time','get_zj_nums','go_to','is_banner',]
    # 搜索的字段，不要添加时间搜索
    search_fields = ['name', 'desc', 'detail', 'degree','learn_time','students','fav_nums','image','click_nums']
    # 过滤
    list_filter = ['name', 'desc', 'detail', 'degree','learn_time','students','fav_nums','image','click_nums','add_time']

    # list_editable = ['is_banner','name','desc'] #在列表页直接进行编辑
    ordering = ['-click_nums'] #默认排序
    readonly_fields = ['fav_nums'] #只读，后台不能修改
    exclude = ['click_nums']  #不显示 字段
    inlines = [LessonInline,CourseResourceInline]  #在课程编辑页面加入章节信息（查看、添加、删除）
    style_fields = {'detail':'ueditor'}
    import_excel = True
    refresh_times = [3,5]

    model_icon = 'fa fa-folder'

    def queryset(self):
        qs = super(CourseAdmin,self).queryset()
        qs = qs.filter(is_banner = False)
        return qs

    def save_models(self):
        #在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()

    def post(self,request,*args,**kwargs):
        if 'excel' in request.FILES:
            pass
        return super(CourseAdmin,self).post(request,args,kwargs)


class BannerCourseAdmin(object):
    list_display = ['name', 'desc', 'detail', 'degree','learn_time','students','fav_nums','image','click_nums','add_time']
    search_fields = ['name', 'desc', 'detail', 'degree','learn_time','students','fav_nums','image','click_nums']
    list_filter = ['name', 'desc', 'detail', 'degree','learn_time','students','fav_nums','image','click_nums','add_time']
    ordering = ['-click_nums'] #默认排序
    readonly_fields = ['fav_nums'] #只读，后台不能修改
    exclude = ['click_nums']  #不显示 字段
    inlines = [LessonInline,CourseResourceInline]  #在课程编辑页面加入章节信息（查看、添加、删除）
    style_fields = {'detail':'ueditor'}

    def queryset(self):
        qs = super(BannerCourseAdmin,self).queryset()
        qs = qs.filter(is_banner = True)
        return qs

    def save_models(self):
        #在保存课程的时候统计课程机构的课程数
        obj = self.new_obj
        obj.save()
        if obj.course_org is not None:
            course_org = obj.course_org
            course_org.course_nums = Course.objects.filter(course_org=course_org).count()
            course_org.save()



class LessonAdmin(object):
    list_display = ['course','name','add_time']
    search_fields = ['course','name']
    #有外键的情况下 用'__name' 在xadmin--过滤器中可以按课程名称搜索该课程所有章节
    list_filter = ['course__name','name','add_time']


class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson__name', 'name', 'add_time']


class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'download','add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name','download', 'add_time']


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(BannerCourse,BannerCourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(Video,VideoAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)
