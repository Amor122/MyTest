from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('human_management/', include('human_management.urls', namespace='human_management')),
    path('test_management/', include('test_management.urls', namespace='test_management')),
    path('admin/', admin.site.urls),
]
