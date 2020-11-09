from django.db import models
import random

def default_sign():
    signs=['孤独的一个人在旅行','在路上....','敢问路在何方？','明天我要去哪里？','下一站！出发！']
    return random.choice(signs)

# Create your models here.
class UserProfile(models.Model):
    username=models.CharField( '用户名',max_length=30,primary_key=True)
    nickname=models.CharField('昵称',max_length=50)
    email=models.EmailField('邮箱')
    password=models.CharField('密码',max_length=32)
    sign=models.CharField('个人签名',max_length=50,default= default_sign)
    info=models.CharField("个人简介",max_length=150,default="")
    avatar=models.ImageField("头像",upload_to="avatar",null=True)
    create_time=models.DateTimeField("创建时间",auto_now_add=True)
    update_time=models.DateTimeField("修改时间",auto_now=True)
    phone=models.CharField("手机",max_length=11,default="")
    class Meta:
        db_table ='user_user_profile'
