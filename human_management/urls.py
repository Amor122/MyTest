from django.contrib import admin
from django.urls import path
from . import views

app_name = 'human_management'

urlpatterns = [
    # 登录页
    path('management_login', views.management_login, name='management_login'),
    # 注销
    path('management_login_out', views.management_login_out, name='management_login_out'),
    # 欢迎页
    path('management_welcome', views.management_welcome, name='management_welcome'),
    # 登录校验
    path('management_login_handle', views.management_login_handle, name='management_login_handle'),
    path('test_page', views.test_page, name='test_page'),
]
