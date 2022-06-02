from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('human_management/',include('human_management.urls')),
    path('test_management/',include('test_management.urls')),
    path('admin/', admin.site.urls),
]
