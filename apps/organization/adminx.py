# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/2 12:56'
import xadmin

from .models import CityDict,CourseOrg,Teacher


class CityDictAdmin(object):
    list_display = ['name', 'desc','add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc','add_time']


class CourseOrgAdmin(object):
    list_display = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city', 'add_time']
    search_fields = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city']
    list_filter = ['name', 'desc', 'click_num', 'fav_nums', 'image', 'address', 'city', 'add_time']
    # relfield_style = 'fk-ajax'


class TeacherAdmin(object):
    list_display = ['org','name', 'work_years', 'work_company']
    search_fields = ['org','name', 'work_years', 'work_company']
    list_filter = ['org__name','name', 'work_years', 'work_company']


xadmin.site.register(CityDict,CityDictAdmin)
xadmin.site.register(CourseOrg,CourseOrgAdmin)
xadmin.site.register(Teacher,TeacherAdmin)