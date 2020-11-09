from django.urls import path
from . import views

urlpatterns = [
    # 127.0.0.1:8000/hotel/query
    path('query',views.get_info),
    #支付宝
    path('bao_pay/',views.BaoView.as_view())
 ]
