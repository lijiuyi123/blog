from django.http import HttpResponseRedirect,request
from django.shortcuts import render
from django.views.generic import ListView,DetailView
import markdown

from blog import models
import time

# Create your views here.


class IndexView(ListView):
    model = models.Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context =super(IndexView, self).get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.all()
        context['time'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        context['blog_category_learn'] = models.Blog.objects.filter(category__category__contains='技术随笔').count()
        context['blog_category_life'] = models.Blog.objects.filter(category__category__contains='生活笔记').count()
        context['archive']=models.Blog.objects.datetimes('created_time','month',order='DESC',)
        return context



def detailblogview(request, blogid):
    blog=models.Blog.objects.get(pk=blogid)
    tags = models.Tag.objects.all()
    blog_category_learn = models.Blog.objects.filter(category__category__contains='技术随笔').count()
    blog_category_life = models.Blog.objects.filter(category__category__contains='生活笔记').count()
    blog.view_count += 1
    blog.save()
    blog.content = markdown.markdown(blog.content,extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',])
    context = {
        'blog' : blog,
        'tags' : tags,
        'blog_category_learn' : blog_category_learn,
        'blog_category_life' :blog_category_life,
    }
    return render(request,'detail.html',context=context)


class LearnView(IndexView):
    model = models.Blog
    queryset = models.Blog.objects.filter(category__category__contains='技术随笔')


class LifeView(IndexView):
    model = models.Blog
    queryset = models.Blog.objects.filter(category__category__contains='生活笔记')