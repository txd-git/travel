from django.urls import path
from .import views
urlpatterns=[
    path('seacher_view/<str:address>', views.get_view),  #添加
    path('view',views.get_viewlist),
    path('view/<str:address>',views.return_address),
    path('views/<str:address>',views.get_data),

]