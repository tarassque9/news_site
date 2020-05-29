from django.contrib import admin
from django.urls import path, include
from .views import redirect_news

urlpatterns = [
    path('', redirect_news),
    path('admin/', admin.site.urls, name='admin'),
    path('news/', include('news.urls'))
]