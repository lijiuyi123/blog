from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView
from blog import models


# Create your views here.


class IndexView(ListView):
    model = models.Blog
    template_name = 'base.html'
    context_object_name = 'blogs'
    paginate_by = 1

    def get_context_data(self, *, object_list=None, **kwargs):
        context =super(IndexView, self).get_context_data(**kwargs)
        context['tags'] = models.Tag.objects.all()
        return context

