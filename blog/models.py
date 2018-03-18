from django.db import models
from django.forms import ModelForm
from ckeditor import fields
from martor.models import  MartorField
# Create your models here.


class Tag(models.Model):

    tag = models.CharField(max_length=20, verbose_name='标签')

    def __str__(self):
        return  self.tag

    class Meta:
        db_table = '标签'
        verbose_name_plural = '博客标签'


class Category(models.Model):

    category = models.CharField(max_length=20, verbose_name='分类')

    def __str__(self):
        return self.category

    class Meta:
        db_table = '分类'
        verbose_name_plural = '博客分类'


class Blog(models.Model):

    title = models.CharField(max_length=50, verbose_name='题目')
    content = MartorField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    changed_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='分类')
    view_count=models.IntegerField(default=0,verbose_name='阅读量')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_time']
        db_table = '博客'
        verbose_name_plural = '博客'

