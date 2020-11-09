import time

from django.db import models

# Create your models here.
from article.models import ArticlePost
from user.models import UserProfile


class Message(models.Model):
    content = models.CharField('内容', max_length=50)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    p_id = models.IntegerField('对应评论的ID', default=0)
    article = models.ForeignKey(ArticlePost, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    class Meta:
        db_table = "message"
