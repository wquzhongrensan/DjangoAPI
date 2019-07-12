from django.urls import re_path
from . import views

app_name = 'users'

urlpatterns = [
    # 新用户注册
    re_path(r'^register/$', views.register, name='register'),

    # 用户登录
    re_path(r'^login/$', views.login, name='login'),

    # 用户信息查询
    re_path(r'^user/(?P<pk>\d+)/profile/$', views.profile, name='profile'),

    # 用户信息编辑
    re_path(r'^user/(?P<pk>\d+)/profile/update/$', views.profile_update, name='profile_update'),

    # 用户密码更改
    re_path(r'^user/(?P<pk>\d+)/pwdchange/$', views.pwd_change, name='pwd_change'),

    # 用户登出接口
    re_path(r'^logout/$', views.logout, name='logout'),
]
