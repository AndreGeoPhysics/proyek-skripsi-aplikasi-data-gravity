from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import InputForm
from .models import InputModel, GravityTable
import json
import pandas as pd

def upload(request):
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            delim = request.POST['delimiter']
            form.save() 
            uploaded_data = f"./storage/upload/{request.FILES['data_input']}"
            file_df = handle_file(uploaded_data, delim)
            model_builder(file_df)
            return render(request, 'success.html')
        else:
            print(form.errors)
            print(request.FILES)
            return HttpResponseRedirect('./')
    else:  
        form = InputForm()
    return render(request, 'gravity_input.html', {
        'form': form
    }) 

def handle_file(file_input, delim=','):
    try:
        df = pd.read_csv(file_input, sep=delim)
        column = df.count(axis='columns')
        if column[0] == 4:
            return df
        else:
            return print('jumlah kolom data harus 4')
    except:
        print('data tidak terbaca')
    
def model_builder(df):
    x = json.dumps(df.iloc[:,0].values.tolist())
    y = json.dumps(df.iloc[:,1].values.tolist())
    z = json.dumps(df.iloc[:,2].values.tolist())
    FA = json.dumps(df.iloc[:,3].values.tolist())
    data = GravityTable(x=x, y=y, z=z, FA=FA)
    data.save()  