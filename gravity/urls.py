from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'gravity'

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('density/', views.upload, name='density'),
    path('sba/', views.upload, name='sba'),
    path('svd/', views.upload, name='svd'),   
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)