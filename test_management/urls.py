from django.urls import path
from . import views, views_organization, views_test

app_name = 'test_management'
urlpatterns = [
    # 人员管理界面
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

    # 组织管理界面
    path('show_organization', views_organization.show_organization),
    path('show_organization2', views_organization.show_organization2),
    path('get_organization_info', views_organization.get_organization_info),
    path('get_organization_dict_info', views_organization.get_organization_dict_info),
    path('get_organization_by_name', views_organization.get_organization_by_name),
    path('delete_organization_by_id', views_organization.delete_organization_by_id),
    path('edit_organization_by_id', views_organization.edit_organization_by_id),
    path('add_organization', views_organization.add_organization),
    path('get_organization_types', views_organization.get_organization_types),
    path('get_organization_tree', views_organization.get_organization_tree),

    # 考试安排界面
    path('get_test', views_test.get_test),
    path('show_test', views_test.show_test),
    path('get_test_selections', views_test.get_test_selections),
    path('edit_test_by_id', views_test.edit_test_by_id),
    path('add_test', views_test.add_test),
    path('delete_test_by_id', views_test.delete_test_by_id),
    path('get_people/<test_id>/', views_test.get_people),

]
