from django.contrib import admin
from django.urls import path
from gravity.views import *
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
    path('dashboard/workspace/<current_id>/get-topo', get_topo, name='get_topo'),
    path('dashboard/workspace/<current_id>/get-bouguer', get_bouguer, name='get_bouguer'),
    path('dashboard/workspace/<current_id>/bouguer-map', bouguer_map, name='bouguer_map'),
    path('dashboard/workspace/<current_id>/get-spectrum', get_spectrum, name='get_spectrum'),
    path('dashboard/workspace/<current_id>/get-fhd', get_fhd, name='get_fhd'),
    path('dashboard/workspace/<current_id>/get-svd', get_svd, name='get_svd'),
    path('save-grid/<current_id>', save_grid, name='save_grid'),
    path('dashboard/testing', testing, name='testing'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)