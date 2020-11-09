from django.urls import path
from .import views
urlpatterns=[
    path('jump/',views.JumpView.as_view()),
    path('result/',views.ResultView.as_view()),
    # path('payorder/',views.get_order_info),
    # path('payorder_info/',views.get_order_page)
]