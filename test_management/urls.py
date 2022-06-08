from django.contrib import admin
from django.urls import path
from . import views

app_name = 'test_management'
urlpatterns = [
    path('show_human', views.show_human),
    path('get_human', views.get_human)
]
