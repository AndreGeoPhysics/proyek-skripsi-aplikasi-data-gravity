from django.db import models
from django.contrib.auth import get_user_model

class GravityTable(models.Model):
    user_id = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    nama_proyek = models.CharField(max_length=100, null=True)
    tanggal = models.DateTimeField(auto_now_add=True, null=True)
    x = models.TextField(null=True)
    y = models.TextField(null=True)
    z = models.TextField(null=True)
    FreeAir = models.TextField(null=True)
    density = models.TextField(null=True)
    sba = models.TextField(null=True)
      
        def __str__(self):
        return self.nama_proyek