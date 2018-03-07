from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from blog import models
import time

# Create your views here.


class IndexView(ListView):
    model = models.Blog
    template_name = 'base.html'
    context_object_name = 'blogs'
    paginate_by = 3

    def get_context_data(self, *, object_list=None, **kwargs):
        context =super(IndexView, self).get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.all()
        context['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        context['blog_category_learn'] = models.Blog.objects.filter(category__category__contains='技术随笔').count()
        context['blog_category_life'] = models.Blog.objects.filter(category__category__contains='生活笔记').count()
        archive_ = models.Blog.objects.datetimes('created_time','month',order='DESC',)
        archive = []
        for i in archive_:
            archive.append(str(i)[:7])
        context['archive']=archive
        return context

