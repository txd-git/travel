from django.urls import path
from . import views
urlpatterns =[
    #验证
    path('ver_code',views.ver_code),
    # 127.0.0.1:8000/user/login
    path('login', views.login),
    # 127.0.0.1:8000/user/register
    path('register', views.register),
]