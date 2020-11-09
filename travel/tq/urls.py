from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/tq/query
    path('query', views.get_location),
    path('get_addree/<str:position>',views.get_addree),
    # 127.0.0.1:800/tq/get_weather/
    path('get_weather/<str:position>', views.get_weather),
    path('get_name',views.get_name)
]
