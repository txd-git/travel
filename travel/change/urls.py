from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('change_user_info/<str:username>',views.change_user_info),
    path('change_info/<str:username>',views.changeinfo),
    path('change_avatar/<str:username>/avatar',views.change_avatar)
]
