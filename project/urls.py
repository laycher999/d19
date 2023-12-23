from django.contrib import admin
from django.urls import path, include
from board.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tinymce/', include('tinymce.urls')),
    path('', index, name='index'),
    path('board/', include('board.urls')),
    path('', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),
]