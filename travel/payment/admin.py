from django.contrib import admin
from .models import TicketPay
# Register your models here.

class Alipay(admin.ModelAdmin):
    list_display = ['order_id','trade_no','order_status','order_buytime','spend_buytime','is_consumed','user']



admin.site.register(TicketPay, Alipay)