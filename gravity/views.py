from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import InputForm
from .models import InputModel, GravityTable
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import json
import pandas as pd

def sign_up(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User berhasil dibuat!")
            return redirect('sign_up')
        else:
            messages.error(request, "Terjadi kesalahan!")
            return redirect('sign_up')
    else:
        form = UserCreationForm()
        konteks = {
            'form': form,
        }
    return render(request, 'sign-up.html', konteks)

def upload_file(request):
    if request.method == 'POST':
        form = InputForm(request.POST, request.FILES)
        if form.is_valid():
            delim = request.POST['delimiter']
            form.save() 
            uploaded_data = f"./storage/upload/{request.FILES['data_input']}"
            file_df, check, pesan = handle_file(uploaded_data, delim)
            if check == True:
                model_builder(file_df)
            else:
                pass
            form = InputForm()
            konteks = {
            'form' : form,
            'pesan' : pesan,
            }
            return render(request, 'upload-file.html', konteks)
    else:  
        form = InputForm()
        konteks = {
            'form': form,
        }
    return render(request, 'upload-file.html', konteks)

def handle_file(file_input, delim=','):
    try:
        df = pd.read_csv(file_input, sep=delim)
        column = df.count(axis='columns')
        if column[0] == 4:
            return df, True, "data berhasil disimpan"
        else:

            return file_input, False, 'jumlah kolom data harus 4'
    except:
        return file_input, False, 'data tidak terbaca'
    
def model_builder(df):
    x = json.dumps(df.iloc[:,0].values.tolist())
    y = json.dumps(df.iloc[:,1].values.tolist())
    z = json.dumps(df.iloc[:,2].values.tolist())
    FA = json.dumps(df.iloc[:,3].values.tolist())
    data = GravityTable(x=x, y=y, z=z, FA=FA)
    data.save()   