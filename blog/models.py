from django.db import models
from django.forms import ModelForm

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
    content = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    #look_count = models.IntegerField()
    changed_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')
    tag = models.ManyToManyField(Tag,verbose_name='标签')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,verbose_name='分类')
    #comment = models.ForeignKey('Comment',on_delete=models.CASCADE,verbose_name='评论')

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-changed_time']
        db_table = '博客'
        verbose_name_plural = '博客'


class Comment(models.Model):

    name = models.CharField(max_length=20,verbose_name='昵称')
    email = models.EmailField(verbose_name='电子邮件')
    comment = models.TextField(verbose_name='评论')

    class Meta:
        verbose_name_plural = '评论'
        db_table = '评论'


class CommentForm(ModelForm):

    class Meta:
        model = Tag
        fields = ['tag']

