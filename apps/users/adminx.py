# -*- coding:utf-8 -*-

import xadmin
from xadmin import views
from xadmin.plugins.auth import UserAdmin

from .models import EmailVerifyRecord,PageBanner,UserProfile


class UserProfileAdmin(UserAdmin):
    def get_form_layout(self):
        if self.org_obj:
            self.form_layout = (
                Main(
                    Fieldset('',
                             'username', 'password',
                             css_class='unsort no_title'
                             ),
                    Fieldset(_('Personal info'),
                             Row('first_name', 'last_name'),
                             'email'
                             ),
                    Fieldset(_('Permissions'),
                             'groups', 'user_permissions'
                             ),
                    Fieldset(_('Important dates'),
                             'last_login', 'date_joined'
                             ),
                ),
                Side(
                    Fieldset(_('Status'),
                             'is_active', 'is_staff', 'is_superuser',
                             ),
                )
            )
        return super(UserAdmin, self).get_form_layout()


class BaseSetting(object):# 创建xadmin的最基本管理器配置，并与view绑定
    enable_themes = True  # 开启主题功能
    use_bootswatch = True


class GlobalSettings(object):   # 全局修改，固定写法
    site_title = '慕学后台管理系统'
    site_footer = '慕学在线网'
    #子菜单收起
    menu_style = 'accordion'


class EmailVerifyRecordAdmin(object):
    list_display = ['code','email','send_type','send_time']
    #可以通过表中指定的类型 进行搜索
    search_fields = ['code','email','send_type']
    #通过时间来筛选
    list_filter = ['code','email','send_type','send_time']
    model_icon = 'fa fa-envelope-open'

class PageBannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index','add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index','add_time']


# xadmin.site.register(UserProfile,UserProfileAdmin)
xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(PageBanner,PageBannerAdmin)
xadmin.site.register(views.BaseAdminView,BaseSetting)# 将基本配置管理与view绑定
xadmin.site.register(views.CommAdminView,GlobalSettings)
