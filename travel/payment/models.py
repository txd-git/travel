from django.db import models
from user.models import UserProfile

# Create your models here.

class TicketPay(models.Model):
    order_id=models.CharField('订单编号',max_length=50)
    trade_no=models.CharField('支付宝交易编号',max_length=100)
    order_status=models.CharField('支付结果',max_length=60)
    order_buytime=models.DateField('购买日期',auto_now_add=True)
    spend_buytime=models.DateField('消费日期')
    is_consumed=models.BooleanField('是否已消费',default=False)
    user=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
