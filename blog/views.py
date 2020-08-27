from django.shortcuts import render
from django.db.models import Q
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from . models import Category, Blog, Comment
from .forms import CommentForm


from django.http import HttpResponse

# Create your views here.

BLOG_PER_PAGE = 7
STATUS = "published"
"""
def category(request):
    categories = Category.objects.all()
    blogs_categories = {}
    for cat in categories.filter(blog__isnull=False):
            blog = Blog.objects.filter(blog_category__pk=cat.pk).earliest('blog_published')
            blogs_categories[cat] = blog.blog_slug
    return render(request,
                  'blog/categories.html',
                  {'categories':categories,
                   'blog_categories': blogs_categories
                   })
"""

#status eklendi
def single_slug(request, single_slug):
    blogs = [b.blog_slug for b in Blog.objects.all()]
    if single_slug in blogs:
        this_blog = Blog.objects.get(blog_slug=single_slug)
        blogs_series = Blog.objects.filter(blog_category__pk=this_blog.blog_category.pk).filter(blog_status=STATUS)
        blog_index = list(blogs_series).index(this_blog)
        return render(request,
                      'blog/bloglist.html',
                      {'blog': this_blog,
                       'sidebar': blogs_series,
                       'blog_index': blog_index,
                       })

#status eklendi
def blog(request):
    context = {}
    blog = Blog.objects.filter(blog_status=STATUS).order_by('-blog_published')


    page = request.GET.get('page', 1)
    blog_paginator = Paginator(blog, BLOG_PER_PAGE)

    try:
        blog = blog_paginator.page(page)
    except PageNotAnInteger:
        blog = blog_paginator.page(BLOG_PER_PAGE)
    except EmptyPage:
        blog = blog_paginator.page(blog_paginator.num_pages)

    context['blog'] = blog


    return render(request,
                  'blog/blogs.html',
                  context)


def lastblog(request, blog_slug):
    this_blog = Blog.objects.get(blog_slug=blog_slug)

    # Comments:

    comments = Comment.objects.filter(comment_blog__pk=this_blog.pk, comment_reply=None).order_by('-comment_published')

    new_comment = None
    if request.user.is_authenticated:
        if request.method == "POST":
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():
                content = request.POST.get('comment_body')
                #new_comment = comment_form.save(commit=False)
                #new_comment.comment_blog = this_blog
                #new_comment.comment_account = request.user
                reply = request.POST.get('comment_id')
                comment_qs = None
                if reply:
                    comment_qs = Comment.objects.get(id=reply)
                comment = Comment.objects.create(comment_blog=this_blog, comment_account=request.user, comment_body=
                                                 content, comment_reply=comment_qs)
                comment.save()
                return HttpResponseRedirect(request.path)
        else:
            comment_form = CommentForm()
    else:
        comment_form = "giriş"

    return render(request,
                  'blog/lastblog.html',
                  {'blog': this_blog,
                   'comments': comments,
                   'comment_form': comment_form,
                   'new_comment': new_comment})


#status eklendi
def get_blog_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = Blog.objects.filter(
            Q(blog_title__icontains=q) |
            Q(blog_content__icontains=q)
        ).filter(blog_status=STATUS).distinct()

        for post in posts:
            queryset.append(post)
        return list(set(queryset))

