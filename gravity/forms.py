from django.forms import ModelForm
from django import forms

class FileForm(forms.Form):
    nama_proyek = forms.CharField(max_length=100)
    delimiter = forms.CharField(max_length=100)
    file_gravity = forms.FileField(upload_to=)