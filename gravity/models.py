from django.db import models
from django.contrib.auth import get_user_model

class FileModel(models.Model):
    wilayah_ukur = models.CharField(max_length=100, null=True)
    user_id = models.ForeignKey(get_user_model(), null=True, on_delete=models.CASCADE)
    file_input = models.FileField(upload_to='')
    delimiter = models.CharField(max_length=100)
    tanggal = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.wilayah_ukur

class DataModel(models.Model):
    file_id = models.ForeignKey(FileModel, null=True, on_delete=models.CASCADE)
    x = models.TextField(null=True)
    y = models.TextField(null=True)
    z = models.TextField(null=True)
    FA = models.TextField(null=True)
      
