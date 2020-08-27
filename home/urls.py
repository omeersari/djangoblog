
from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('about/', views.about, name='about'),
    path('search/', views.search_view, name='search'),

]
