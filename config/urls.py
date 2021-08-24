from django.contrib import admin
from django.urls import path
from gravity.views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', login, name='login'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload-file/', upload_file, name='upload_file'),
    path('ubah-file/', ubah_file, name='ubah_file'),
    path('hapus-file/', hapus_file, name='hapus_file'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)