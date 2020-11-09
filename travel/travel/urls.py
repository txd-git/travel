"""travel URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 首页127.0.0.1:8000/travel
    path('travel', views.travel),
    path('travel2', views.travel2),

    # 关于我们 127.0.0.1:8000/contact
    # path('contact/',include('contact.urls')),
    # 天气模块
    path('tq/', include('tq.urls')),
    # 用户模块
    path('user/', include('user.urls')),
    # 酒店支付模块
    path("hotel/", include('hotel.urls')),
    # 127.0.0.1:8000/v1/customized/view
    path('v1/customized/', include('customized.urls')),
    path('payment/', include('payment.urls')),

    path('change/', include('change.urls')),
    # 论坛模块
    path('article/', include('article.urls')),
    path('message/',include('message.urls'))
]
# urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
