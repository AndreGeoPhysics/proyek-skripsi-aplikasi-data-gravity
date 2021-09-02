from django.contrib import admin
from .models import GravityTable

@admin.register(GravityTable)
class GravityTableAdmin(admin.ModelAdmin):
    list_display = ( 'unique_id', 'user_id', 'nama_proyek', 'tanggal', 'x', 'y', 'z', 'freeair', 'density', 'sba')
    