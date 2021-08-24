from django.forms import ModelForm
from django import forms
from gravity.models import FileModel

class FileForm(forms.ModelForm):
    class Meta:
        model = FileModel
        exclude = ('user_id',) 

        widgets = {
            'wilayah_ukur' : forms.TextInput({'class':'form-control'}),
            'file_input' : forms.FileInput({'class':'form-control'}),
            'delimiter' : forms.TextInput({'class':'form-control'}),
        }