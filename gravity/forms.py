from django import forms

class FileForm(forms.Form):
    nama_input = forms.CharField(max_length=100)
    delimiter = forms.CharField(max_length=100)
    file_gravity = forms.FileField()

    def __str__(self):
        return self.nama_input

GRID_CHOICES =(
    ("2", "2"),
    ("4", "4"),
    ("8", "8"),
    ("16", "16"),
    ("32", "32"),
    ("64", "64"),
    ("128", "128"),
    ("256", "256"),
    ("512", "512"),
)

class GridForm(forms.Form):
    ngrid = forms.ChoiceField(label='jumlah grid', choices=GRID_CHOICES)
    sample_interval = forms.IntegerField(label='interval sampel', max_value=1000)

    def __str__(self):
        return self.ngrid