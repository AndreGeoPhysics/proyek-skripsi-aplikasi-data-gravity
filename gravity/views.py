from django.shortcuts import render, redirect, HttpResponse
from .forms import FileForm
from .models import FileModel, DataModel
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
import json
import pandas as pd

@login_required(login_url=settings.LOGIN_URL)
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

@login_required(login_url=settings.LOGIN_URL)
def dashboard(request):
    rincian = FileModel.objects.filter(user_id=request.user)
    konteks = {
        'rincian': rincian,
    }
    return render(request, 'dashboard.html', konteks)

@login_required(login_url=settings.LOGIN_URL)
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            delim = request.POST['delimiter']
            obj = form.save(commit=False) 
            uploaded_data = request.FILES['file_input']
            print(uploaded_data)
            file_df, check, pesan = handle_file(uploaded_data, delim)
            if check == True:
                obj.user_id = request.user
                obj.save()
                model_builder(file_df)
            else:
                pass
            form = FileForm()
            konteks = {
            'form' : form,
            'pesan' : pesan,
            }
            return render(request, 'upload-file.html', konteks)
    else:  
        form = FileForm()
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
    data = DataModel(x=x, y=y, z=z, FA=FA)
    data.save()   