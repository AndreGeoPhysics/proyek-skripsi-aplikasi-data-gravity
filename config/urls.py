from django.contrib import admin
from django.urls import path
from gravity.views import *
from gravity.processing import processing_data
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView, LogoutView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('sign-up/', sign_up, name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('upload-file/', upload_file, name='upload_file'),
    path('dashboard/workspace/<current_id>', workspace, name='workspace'),
    path('dashboard/hapus/<current_id>', hapus_file, name='hapus_file'),
    path('dashboard/workspace/<current_id>/get-bouger', get_bouger, name='get_bouger'),
    path('dashboard/workspace/<current_id>/get-density', get_density, name='get_density'),
    path('dashboard/workspace/<current_id>/processing-data', processing_data, name='processing_data'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)