from django.contrib import admin
from tinymce.widgets import TinyMCE
from django.db import models
from .models import Category, Blog, Comment

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"category_slug": ('category_title',)}

    list_display = ['category_title', 'id', 'category_last_updated']

    list_filter = ['category_title']


class BlogAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }
    prepopulated_fields = {"blog_slug": ('blog_title',)}

    list_display = ['blog_title', 'id', 'get_category',  'blog_published', 'blog_updated', 'blog_status']
    list_editable = ['blog_status']
    search_fields = ['blog_title', 'blog_category__category_title']
    list_filter = ['blog_status']

    def get_category(self, obj):
        return obj.blog_category
    get_category.short_description = 'Category'



class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'comment_blog', 'comment_account', 'comment_published', 'comment_reply_id']
    list_filter = ['comment_blog', 'comment_account']
    search_fields = ['comment_blog', 'comment_account', 'comment_published']

admin.site.register(Category, CategoryAdmin)
admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment, CommentAdmin)




