from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from django.conf import settings
import datetime

DEFAULT_STATUS = "draft"
STATUS = [
    # left side: DB
    # right side: human-readable name
    ('draft', 'Taslak'),
    ('published', 'Yayınlandı'),
    ('deleted', 'Silindi'),
]

DEFAULT_COMMENT_STATUS = 'published'
COMMENT_STATUS = [
    ('published', 'Yayınlandı'),
    ('deleted', 'Silindi'),
]


class Category(models.Model):
    category_title = models.CharField(max_length=200)
    category_content = models.CharField(max_length=200)
    category_slug = models.SlugField(default="")
    category_last_updated = models.DateField(default=timezone.now)
    category_img = models.ImageField(blank=True, null=True, upload_to='cat_images')

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.category_title


class Blog(models.Model):
    blog_category = models.ForeignKey(Category, on_delete=models.CASCADE)
    blog_title = models.CharField(max_length=200)
    blog_content = models.TextField()
    blog_slug = models.SlugField(default="")
    blog_published = models.DateTimeField(default=timezone.now)
    blog_updated = models.DateTimeField(auto_now=True)
    blog_status = models.CharField(
        default=DEFAULT_STATUS,
        choices=STATUS,
        max_length=10,
    )

    def __str__(self):
        return self.blog_title

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.blog_slug = slugify(self.blog_title)

        super(Blog, self).save(*args, **kwargs)

    def ends_within_7_days(self):
        today = datetime.datetime.now().date()
        published_day = self.blog_published.date()
        return (today - published_day).days <= 7

class Comment(models.Model):
    comment_blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    comment_account = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE, related_name='accounts')
    comment_body = models.TextField()
    comment_published = models.DateTimeField(auto_now_add=True)
    comment_status = models.CharField(
        default=DEFAULT_COMMENT_STATUS,
        choices=COMMENT_STATUS,
        max_length=10,
    )
    comment_reply = models.ForeignKey('self', null=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['comment_published']

    def __str__(self):
        return f"{self.comment_account} - {self.comment_blog}"
