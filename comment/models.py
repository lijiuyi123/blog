from django.db import models
from  blog.models import Blog
# Create your models here.


class Comment(models.Model):
    name = models.CharField(max_length=20, verbose_name='名称')
    email = models.EmailField(verbose_name='电子邮件')
    comment = models.TextField(verbose_name='评论')
    create_time = models.DateTimeField(verbose_name='时间')
    commentinblog = models.ForeignKey(Blog,on_delete=models.CASCADE)



