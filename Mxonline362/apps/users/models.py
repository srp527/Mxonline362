#-*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name=u'昵称',default=' ')
    birday = models.DateField(verbose_name=u'生日',null=True,blank=True)
    gender = models.CharField(max_length=6,choices=(('male',u'男'),('female',u'女')),default=' ')
    address =models.CharField(max_length=100,default=' ')
    mobile = models.CharField(max_length=11,null=True,blank=True)
    image = models.ImageField(upload_to='image/%Y/%m',default=u'image/default.png',max_length=100)

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def get_unread_nums(self): #获取用户未读消息的数量
        from operation.models import UserMessage
        return UserMessage.objects.filter(user=self.id,has_read=False).count()


    def __str__(self):
        return self.username


class EmailVerifyRecord(models.Model): #邮箱验证码 表格
    code = models.CharField(max_length=20,verbose_name=u'验证码')
    email = models.EmailField(max_length=50,verbose_name=u'邮箱')
    send_type = models.CharField(choices=(('register',u'注册'),('forget',u'找回密码'),('update_email',u'修改邮箱')),max_length=20,verbose_name=u'验证码类型')
#注意： now()去掉括号才会根据class实例化的时间来生成时间
    send_time = models.DateTimeField(default=datetime.now,verbose_name=u'发送时间')

    class Meta:
        verbose_name = u'邮箱验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{0}({1})'.format(self.code,self.email)


class PageBanner(models.Model): #轮播图
    #轮播图标题
    title = models.CharField(max_length=100,verbose_name=u'标题')
    #在数据库中存储的是图片路径  非图片
    image = models.ImageField(upload_to='banner/%Y/%m',verbose_name=u'轮播图',max_length=100)
    url = models.URLField(max_length=200,verbose_name=u'访问地址')
    #轮播图的顺序控制，用数字来排序
    index = models.IntegerField(default=100,verbose_name=u'顺序')
    add_time = models.DateTimeField(default=datetime.now,verbose_name=u'添加时间')

    class Meta:
        verbose_name = u'轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
