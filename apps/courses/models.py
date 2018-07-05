#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from DjangoUeditor.models import UEditorField

from django.db import models
from organization.models import CourseOrg,Teacher


# Create your models here.
class Course(models.Model):
    #后添加外键 加null，blank目的：防止加外键前已添加的课程报错，（允许为空）
    course_org = models.ForeignKey(CourseOrg, verbose_name=u'课程机构', null=True, blank=True,on_delete=models.CASCADE,)
    teacher = models.ForeignKey(Teacher, verbose_name=u'课程讲师', null=True, blank=True,on_delete=models.CASCADE,)
    category = models.CharField(max_length=20, verbose_name=u'课程类别', default=u'后端开发')
    name = models.CharField(max_length=50,verbose_name=u'课程名称')
    desc = models.CharField(max_length=300,verbose_name=u'课程描述')
    is_banner = models.BooleanField(default=False,verbose_name=u'是否轮播')
    #TextField不限长度
    # detail = models.TextField(verbose_name=u'课程详情')
    detail = UEditorField(verbose_name=u'课程详情',width=600,height=300,

                                         imagePath='courses/ueditor/',
                                         filePath='courses/ueditor/',default='')
    degree = models.CharField(verbose_name=u'难度',choices=(('cj','初级'),('zj','中级'),('gj','高级')),max_length=2)
    learn_time = models.IntegerField(default=0,verbose_name=u'学习时长(分钟数)')
    students = models.IntegerField(default=0,verbose_name=u'学习人数')
    fav_nums = models.IntegerField(default=0,verbose_name=u'收藏人数')
    image = models.ImageField(upload_to='courses/%Y/%m',verbose_name=u'封面图',max_length=100)
    click_nums = models.IntegerField(default=0,verbose_name=u'点击数')
    #tag 设置一个标签，相关推荐里用到
    tag = models.CharField(default='',verbose_name=u'课程标签',max_length=20)
    youneed_know = models.CharField(max_length=30, verbose_name=u'课程须知--讲师', default='')
    youcan_learn = models.CharField(max_length=30, verbose_name=u'课程能学到的知识--讲师', default='')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')


    class Meta:
        verbose_name = u'课程'
        verbose_name_plural = verbose_name

    def get_zj_nums(self): #获取课程章节数
        all_lessons_nums = self.lesson_set.all().count()
        return all_lessons_nums
    get_zj_nums.short_description = '章节数'

    def go_to(self):
        from django.utils.safestring import mark_safe #直接将文本显示
        return mark_safe("<a href='http://www.baidu.com'>跳转</>")
    go_to.short_description = '跳转'

    def get_learn_users(self): #获取课程学习用户
        return self.usercourse_set.all()[:5]

    def get_lessons(self): #获取课程章节
        return self.lesson_set.all()

    def get_course_comments(self): #获取课程所有评论
        return self.coursecomments_set.all()

    def __str__(self):
        return self.name


class BannerCourse(Course):
    #把课程是否轮播在xadmin中单独列出，但与course用一个表
    #即同一个model 注册两个管理器
    class Meta:
        verbose_name = '轮播课程'
        verbose_name_plural = verbose_name
        proxy = True  #True 不再生成新表，不然这个类还会生成一个新表


class Lesson(models.Model):
    #外键 与课程关联  一个课程对应多个章节
    course = models.ForeignKey(Course,verbose_name=u'课程',on_delete=models.CASCADE,)
    name = models.CharField(max_length=100,verbose_name=u'章节名')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'章节'
        verbose_name_plural = verbose_name

    def get_lesson_video(self): #获取该章节所有视频信息
        return self.video_set.all()

    def __str__(self):
        return self.name


class Video(models.Model):
    lesson = models.ForeignKey(Lesson,verbose_name=u'章节',on_delete=models.CASCADE,)
    name = models.CharField(max_length=100, verbose_name=u'视频名')
    url = models.CharField(max_length=200,verbose_name=u'访问地址',default='')
    learn_time = models.IntegerField(default=0, verbose_name=u'学习时长(分钟数)')
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'视频'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):
    course = models.ForeignKey(Course, verbose_name=u'课程',on_delete=models.CASCADE,)
    name = models.CharField(max_length=100, verbose_name=u'名称')
    #FileField 文件类型的 在后台可以直接生成上传的按钮
    download = models.FileField(upload_to='course/resource/%Y/%m',verbose_name=u'资源文件',max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'课程资源'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
