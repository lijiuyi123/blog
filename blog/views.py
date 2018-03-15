from django.http import HttpResponseRedirect, request
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from blog import models
import time
import os
import json
import uuid
from django.conf import settings
from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import markdown
from martor.utils import LazyEncoder


@login_required
def markdown_uploader(request):
    """
    Makdown image upload for locale storage
    and represent as json to markdown editor.
    """
    if request.method == 'POST' and request.is_ajax():
        if 'markdown-image-upload' in request.FILES:
            image = request.FILES['markdown-image-upload']
            image_types = [
                'image/png', 'image/jpg',
                'image/jpeg', 'image/pjpeg', 'image/gif'
            ]
            if image.content_type not in image_types:
                data = json.dumps({
                    'status': 405,
                    'error': _('Bad image format.')
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            if image._size > settings.MAX_IMAGE_UPLOAD_SIZE:
                to_MB = settings.MAX_IMAGE_UPLOAD_SIZE / (1024 * 1024)
                data = json.dumps({
                    'status': 405,
                    'error': _('Maximum image file is %(size) MB.') % {'size': to_MB}
                }, cls=LazyEncoder)
                return HttpResponse(
                    data, content_type='application/json', status=405)

            img_uuid = "{0}-{1}".format(uuid.uuid4().hex[:10], image.name.replace(' ', '-'))
            tmp_file = os.path.join(settings.MARTOR_UPLOAD_PATH, img_uuid)
            def_path = default_storage.save(tmp_file, ContentFile(image.read()))
            img_url = os.path.join(settings.MEDIA_URL, def_path)

            data = json.dumps({
                'status': 200,
                'link': img_url,
                'name': image.name
            })
            return HttpResponse(data, content_type='application/json')
        return HttpResponse(_('Invalid request!'))
    return HttpResponse(_('Invalid request!'))


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
        context['blog_category_learn'] = models.Blog.objects.filter(category__category__contains='技术随笔').count()
        context['blog_category_life'] = models.Blog.objects.filter(category__category__contains='生活笔记').count()
        context['archive'] = models.Blog.objects.datetimes('created_time', 'month', order='DESC', )
        return context


def detailblogview(request, blogid):
    blog = models.Blog.objects.get(pk=blogid)
    tags = models.Tag.objects.all()
    blog_category_learn = models.Blog.objects.filter(category__category__contains='技术随笔').count()
    blog_category_life = models.Blog.objects.filter(category__category__contains='生活笔记').count()
    blog.view_count += 1
    blog.save()
    blog.content = markdown.markdown(blog.content, extensions=[
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
        'markdown.extensions.admonition'
    ])
    context = {
        'blog': blog,
        'tags': tags,
        'blog_category_learn': blog_category_learn,
        'blog_category_life': blog_category_life,
    }
    return render(request, 'detail.html', context=context)


class LearnView(IndexView):
    model = models.Blog
    queryset = models.Blog.objects.filter(category__category__contains='技术随笔')


class LifeView(IndexView):
    model = models.Blog
    queryset = models.Blog.objects.filter(category__category__contains='生活笔记')
