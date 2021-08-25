from django.contrib import admin
from .models import FileModel, DataModel

@admin.register(DataModel)
class DataAdmin(admin.ModelAdmin):
    list_display = ('file_asal', 'x', 'y', 'z', 'FA')

@admin.register(FileModel)
class FileAdmin(admin.ModelAdmin):
    list_display = ('wilayah_ukur', 'user_id', 'file_input', 'delimiter', 'tanggal')
    