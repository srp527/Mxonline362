# -*- coding:utf-8 -*-
from django.apps import AppConfig



class UsersConfig(AppConfig):   #在apps.py里面配置 app的显示名称  在后台管理中显示名
    name = 'users'
    verbose_name = u'用户信息'
