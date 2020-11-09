from django.db import models
from tq.models import City
# Create your models here.
class CityInfo(models.Model):
    city_obj=models.CharField('城市名称',max_length=50)
    view_address=models.CharField('景点地点',max_length=200)
    view_score=models.CharField('景点分数',max_length=20)
    view_price=models.DecimalField('票价',max_digits=7,decimal_places=2)
    view_name=models.CharField('景点名称',max_length=50)
    view_img=models.CharField('景点图片',max_length=400)
    # created_time=models.DateField('创建时间',auto_now_add=True)
    # updated_time=models.DateField('更新时间',auto_now=True)
    # is_active=models.BooleanField('是否活跃',default=True)




# class Meishi(models.Model):
#     pass
