from django.contrib import admin
from django.urls import path
from . import views

app_name = 'test_management'
urlpatterns = [
    path('show_human', views.show_human),
    path('get_human', views.get_human),
    path('edit_human', views.edit_human),
    # 返回组织列表
    path('get_organizations', views.get_organizations),
    # 获取职位信息
    path('get_posts', views.get_posts),
]
