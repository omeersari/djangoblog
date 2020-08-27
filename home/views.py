from django.shortcuts import render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from blog.views import get_blog_queryset
from operator import attrgetter
from blog.models import Category, Blog
import datetime


BLOG_PER_PAGE = 7
STATUS = "published"

#status eklendi
def homepage(request):
    categories = Category.objects.all()

    blogs_categories = {}
    for cat in categories.filter(blog__isnull=False):
        blog = Blog.objects.filter(blog_category__pk=cat.pk).filter(blog_status=STATUS).first()
        if blog:
            blogs_categories[cat] = blog.blog_slug

    blogs = Blog.objects.filter(blog_status=STATUS).order_by('-blog_updated')[:6]
    #last_ten_blogs = reversed(blogs)
    today = datetime.datetime.now()
    return render(request,
                  'home/homepage.html',
                  {'categories': categories,
                   'blog_categories': blogs_categories,
                   'lastblogs': blogs,
                   'today':today
                   })


def about(request):
    return render(request,
                  'home/about.html')


def search_view(request, *args, **kwargs):
    context = {}
    query = ""
    if request.GET:
        query = request.GET.get('q', '')
        context['query'] = str(query)

    blog = sorted(get_blog_queryset(query), key=attrgetter('blog_published'), reverse=True)

    # Pagination
    page = request.GET.get('page', 1)
    blog_paginator = Paginator(blog, BLOG_PER_PAGE)

    try:
        blog = blog_paginator.page(page)
    except PageNotAnInteger:
        blog = blog_paginator.page(BLOG_PER_PAGE)
    except EmptyPage:
        blog = blog_paginator.page(blog_paginator.num_pages)

    context['blog'] = blog


    return render(request, 'home/search.html', context)
