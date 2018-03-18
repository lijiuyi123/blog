from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog import models
import time
import markdown


# Create your views here.


class IndexView(ListView):
    model = models.Blog
    template_name = 'index.html'
    context_object_name = 'blogs'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.all()
        context['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        context['categorys'] = models.Category.objects.all()
        for category in context['categorys']:
            category.count = models.Blog.objects.filter(category__category__contains=category).count()
            category.save()
        return context


class CategoryView(IndexView):

    def get_queryset(self, **kwargs):
        blogs = models.Blog.objects.filter(category__category__contains=self.kwargs['category_url'])
        return blogs


class DetailBlogView(DetailView):
    model = models.Blog
    template_name = 'detail.html'
    context_object_name = 'blog'
    pk_url_kwarg = 'id'

    def get_object(self, queryset=None):
        object = super(DetailBlogView,self).get_object()
        object.view_count += 1
        object.save()
        object.content = markdown.markdown(object.content,
                                         extensions=[
                                             'markdown.extensions.extra',
                                             'markdown.extensions.codehilite',
                                             'markdown.extensions.toc',
                                             'markdown.extensions.fenced_code',
                                             'markdown.extensions.attr_list',
                                             'markdown.extensions.def_list',
                                             'markdown.extensions.tables',
                                             'markdown.extensions.smart_strong',
                                             'markdown.extensions.smarty',
                                             'markdown.extensions.footnotes',
                                             'markdown.extensions.admonition'])
        return object

    def get_context_data(self, **kwargs):
        context = super(DetailBlogView, self).get_context_data()
        context['tags'] = models.Tag.objects.all()
        #context['time'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        context['categorys'] = models.Category.objects.all()
        for category in context['categorys']:
            category.count = models.Blog.objects.filter(category__category__contains=category).count()
            category.save()
        return context
