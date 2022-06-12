from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path, include


def index(request):
    """主页的重定向"""
    return HttpResponseRedirect('/human_management/management_login')


urlpatterns = [
    path('human_management/', include('human_management.urls', namespace='human_management')),
    path('test_management/', include('test_management.urls', namespace='test_management')),
    path('admin/', admin.site.urls),
    path('', index),
]
