from user.models import UserProfile
from django.db import models
from django.utils import timezone

# timezone 用于处理时间相关事务。


# 博客文章数据模型
class ArticlePost(models.Model):
    title = models.CharField('标题', max_length=100, default='标题')
    body = models.TextField('正文',default='分享你的经历')
    img = models.ImageField('图片',upload_to="arttu", null=True)
    created = models.DateTimeField('创建时间',default=timezone.now)
    updated = models.DateTimeField('更新时间',auto_now=True)
    total_views = models.PositiveIntegerField('浏览量',default=0)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "article"
        ordering = ('-created',)
