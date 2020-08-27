
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('home.urls')),
    path('', include('blog.urls')),
    #path('jet_api/', include('jet_django.urls')),
    path('tinymce/', include('tinymce.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
