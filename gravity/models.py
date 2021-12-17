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

class GridTable(models.Model):
    grid_ref = models.OneToOneField(GravityTable, primary_key=True, on_delete=models.CASCADE)
    n_grid = models.IntegerField(null=True)
    sample = models.IntegerField(null=True) 
    x_grid = models.TextField(null=True)
    y_grid = models.TextField(null=True)
    sba_interpolate = models.TextField(null=True)
    elev_interpolate = models.TextField(null=True)
    fa_interpolate = models.TextField(null=True)

    def __str__(self): 
        return "%s grid" % self.grid_ref.unique_id

class SpectralTable(models.Model):
    spectral_ref = models.OneToOneField(GridTable, primary_key=True, on_delete=models.CASCADE)
    k = models.TextField(null=True)
    lnA_1 = models.TextField(null=True)
    lnA_2 = models.TextField(null=True)
    lnA_3 =  models.TextField(null=True)

    def _str_(self):
        return "%s nilai spektral" % self.grid_ref.unique_id