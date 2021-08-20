from django import forms
from .models import InputModel

class InputForm(forms.ModelForm):
    class Meta:
        model = InputModel
        fields = ('pengirim', 'delimiter', 'data_input')