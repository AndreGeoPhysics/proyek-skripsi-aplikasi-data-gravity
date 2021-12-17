from django.contrib import admin
from .models import GravityTable, GridTable, SpectralTable

@admin.register(GravityTable)
class GravityTableAdmin(admin.ModelAdmin):
    list_display = ( 'unique_id', 'user_id', 'nama_proyek', 'tanggal', 'x', 'y', 'z', 'freeair', 'density', 'sba')
    
@admin.register(GridTable)
class GridTableAdmin(admin.ModelAdmin):
    list_display = ('grid_ref', 'n_grid', 'x_grid', 'y_grid', 'sba_interpolate', 'elev_interpolate', 'fa_interpolate')

@admin.register(SpectralTable)
class SpectralTableAdmin(admin.ModelAdmin):
    list_display = ('k', 'lnA_1', 'lnA_2', 'lnA_3')