from django import forms

class FileForm(forms.Form):
    nama_input = forms.CharField(max_length=100)
    delimiter = forms.CharField(max_length=100)
    file_gravity = forms.FileField()

    def __str__(self):
        return self.nama_input