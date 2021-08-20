from django.db import models

class InputModel(models.Model):
    pengirim = models.CharField(max_length=100)
    data_input = models.FileField(upload_to='upload/', default="DEFAULT")
    delimiter = models.CharField(max_length=100)
    
    def __str__(self):
        return self.pengirim 

class GravityTable(models.Model):
    x = models.TextField(null=True)
    y = models.TextField(null=True)
    z = models.TextField(null=True)
    FA = models.TextField(null=True)
      
