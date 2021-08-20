from django.contrib import admin
from .models import GravityTable, InputModel

@admin.register(GravityTable)
class TableAdmin(admin.ModelAdmin):
    list_display = ('x', 'y', 'z', 'FA')

@admin.register(InputModel)
class InputAdmin(admin.ModelAdmin):
    list_display = ('pengirim', 'data_input', 'delimiter')
    