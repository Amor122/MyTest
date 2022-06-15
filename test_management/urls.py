from django.urls import path
from . import views, views_organization

app_name = 'test_management'
urlpatterns = [
    path('show_human', views.show_human),
    path('get_human', views.get_human),
    path('edit_human', views.edit_human),
    path('add_human', views.add_human),
    # 返回组织列表
    path('get_organizations', views.get_organizations),
    # 获取职位信息
    path('get_posts', views.get_posts),
    path('reset_user_password', views.reset_user_password),
    path('delete_user_by_id', views.delete_user_by_id),

    # 组织管理界面示意图
    path('show_organization', views_organization.show_organization),
    path('get_organization_info', views_organization.get_organization_info),
    path('get_organization_dict_info', views_organization.get_organization_dict_info),

]
