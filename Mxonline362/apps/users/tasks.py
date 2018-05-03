# -*- coding:utf-8 -*- 
__author__ = 'SRP'
__date__ = '2018/4/25 15:20'


from random import Random

from django.core.mail import send_mail

from users.models import EmailVerifyRecord
from Mxonline362.settings import EMAIL_FROM
from Mxonline362.celery import app


#生成一个随机字符串  作为邮件激活过程中发送的链接中的一个字符串
def generate_random_str(randomlength=8):
    str = ''
    chars = 'abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ0123456789'
    length = len(chars)-1
    random = Random()
    for i in range(randomlength):
        str+=chars[random.randint(0,length)]
    return str


@app.task
def send_register_email(email,send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'update_email':
        code = generate_random_str(4)
    else:
        code = generate_random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()       #将数据提取存到数据库中，

    email_title = ""
    email_body = ""

    if send_type == 'register':
        email_title = '慕学在线网注册激活链接'
        email_body = '请点击下面的链接激活你的账号：http://srp.wangsir.wang/users/active/{0}'.format(code)

        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == 'forget':
        email_title = '慕学在线网密码重置链接'
        email_body = '请点击下面的链接重置你的密码：http://srp.wangsir.wang/users/reset/{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'update_email':
        email_title = '慕学在线网邮箱修改验证码'
        email_body = '你的邮箱验证码为：{0}'.format(code)

        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
