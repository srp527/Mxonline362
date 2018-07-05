# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/7 18:32'

import re
from django import forms

from operation.models import UserAsk

#正常情况下的Form
# class UserAskForm(forms.Form):
#     name = forms.CharField(required=True,min_length=2,max_length=20)
#     phone = forms.CharField(required=True,min_length=11,max_length=11)
#     course_name = forms.CharField(required=True,min_length=5,max_length=50)



#ModelForm 字段差不多的可以直接继承ModelForm
class UserAskForm(forms.ModelForm):


    class Meta:
        model = UserAsk
        fields = ['name','mobile','course_name' ]

    #这个函数必须已clean开头，对mobile（电话号码)进行验证，
    #在views中实例化的时候对自动执行该函数，实现对mobile的验证
    def clean_mobile(self):
        '''
        验证手机号码是否合法
        '''
        mobile = self.cleaned_data['mobile']
        REGEX_MOBILE = '^1[358]\d{9}$|^147\d{8}$|^176\d{8}$'
        p = re.compile(REGEX_MOBILE)
        if p.match(mobile):
            return mobile
        else:
            raise forms.ValidationError(u'手机号码非法',code='mobile_invalid')

