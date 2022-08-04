from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from xcelcomp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload, name='upload'),
    path('excel/', views.excel_list, name='excel_list'),
    path('excel/upload', views.upload_book, name='upload_book')
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
