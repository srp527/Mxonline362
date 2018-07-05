# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/4 9:43'

from django import forms
from captcha.fields import CaptchaField #验证码 用到的库

from .models import UserProfile

class LoginForm(forms.Form): #定义的username，password名称和html里的要一致
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=5)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=5)
    captcha = CaptchaField(error_messages={"invalid":u'验证码错误'}) #field会生成相应的html代码 input框


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": u'验证码错误'})  # field会生成相应的html代码 input框


class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UeerInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birday','address','mobile']
