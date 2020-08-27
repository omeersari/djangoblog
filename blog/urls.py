from django.contrib import admin
from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    #path('categories/', views.category, name="category"),
    path('blogs/', views.blog, name='blogs'),
    path('blogs/<blog_slug>/', views.lastblog, name='lastblog'),
    path('<single_slug>/', views.single_slug, name='single_slug'),


]