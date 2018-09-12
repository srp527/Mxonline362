# Mxonline362
Django2+python3+nginx+uwsgi  Mxonline

#### 网站主页:http://srp.wangsir.wang

#### 启动 
    python manage runserver

## 目录结构

    Mxonline362/
        |
        |——apps/             #app过多时创建 便于管理  需要设置source root
        |    |
        |    |—courses/       #课程app (课程\轮播课程\视频\课程资源)
        |    |—operation/     #关联app 建立用户和课程之间关联(用户咨询\课程评论\用户收藏\用户消息\用户课程)
        |    |—organization/  #课程机构app(城市\课程机构信息\讲师信息)
        |    |—users/         #用户app (用户信息\邮箱验证码\轮播图)
        |    |—utils/         #email_send定义邮件发送内容\mixin_utils定义登录验证
        |
        |——extra_apps/       #需要设置source root
        |    | 
        |    |—DjangoUeditor/ #富文本 
        |    |—xadmin/        #xadmin后台管理
        |    
        |——media/            #媒体文件目录
        | 
        |——static/           #css\js目录
        |
        |——templates/        #存放前端模板的目录
        |
        |——Mxonline362/      #Django项目总设置目录
        |    |
        |    |—celery.py      #自定义 celery 实现异步发送邮件
        |    |—settings.py    #Django项目全局设置文件
        |    |—urls.py        #到各app的总路由
        |    |—wsgi.py        #WSGI设置
        |
        |——manage.py         #启动 python manage runserver
        | 
        |——log/              #日志存放目录
       
        
        