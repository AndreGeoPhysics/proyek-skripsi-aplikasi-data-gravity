from django.db import models
from django.contrib.auth import get_user_model
import uuid

class GravityTable(models.Model):
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, unique=True)
    user_id = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    url_name = models.TextField(null=True)
    nama_proyek = models.CharField(max_length=100, null=True)
    tanggal = models.DateTimeField(auto_now_add=True, null=True)
    x = models.TextField(null=True)
    y = models.TextField(null=True)
    z = models.TextField(null=True)
    freeair = models.TextField(null=True)
    density = models.TextField(null=True)
    sba = models.TextField(null=True)

    def __str__(self):
        return self.unique_id