from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import FileForm
from .models import GravityTable
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .processing import *
import os
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
    rincian = GravityTable.objects.filter(user_id=request.user)
    konteks = {
        'rincian': rincian,
    }
    return render(request, 'dashboard.html', konteks)

@login_required(login_url=settings.LOGIN_URL)
def workspace(request, current_id):
    work_data = GravityTable.objects.get(unique_id=current_id)
    x, y, z, freeair_anomaly = dbDecode(work_data)
    densitas = work_data.density
    SBA1 = work_data.sba1
    SBA2 = work_data.sba2
    wilayah = work_data.nama_proyek
    plot = processing_data(x, y, z, freeair_anomaly, densitas, SBA1, SBA2, wilayah)
    konteks = {
        'work_data' : work_data,
        'plot' : plot
    }
    return render(request, 'workspace.html', konteks)
 
@login_required(login_url=settings.LOGIN_URL)
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            nama_user = request.user
            nama = request.POST['nama_input']
            delim = request.POST['delimiter']
            uploaded_data = request.FILES['file_gravity']
            file_df, check, pesan = handle_file(uploaded_data, delim)
            if check == True:
                model_id = gravitymodelbuilder(nama_user, nama, file_df)
                handle_uploaded_file(uploaded_data, model_id)
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

def gravitymodelbuilder(nama_user, nama, df):
    user_id = nama_user
    nama_proyek = nama
    x = json.dumps(df.iloc[:,0].values.tolist())
    y = json.dumps(df.iloc[:,1].values.tolist())
    z = json.dumps(df.iloc[:,2].values.tolist())
    freeair = json.dumps(df.iloc[:,3].values.tolist())
    data = GravityTable(user_id=user_id, nama_proyek=nama_proyek, x=x, y=y, z=z, freeair=freeair)
    data.save()
    return data.unique_id  

def handle_uploaded_file(f, db_id):
    url_name = f'gravity/simpan/{db_id}{f.name}'
    with open(url_name, 'wb+') as destination:  
        for chunk in f.chunks():
            destination.write(chunk)
    db = GravityTable.objects.get(unique_id=db_id)
    db.url_name = url_name
    db.save()

@login_required(login_url=settings.LOGIN_URL)
def hapus_file(request, current_id):
    target = GravityTable.objects.get(unique_id=current_id)
    os.remove(target.url_name)
    target.delete()
    return redirect('dashboard')

def get_density(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    current_density = table_data.density
    if current_density is None:
        x, y, z, freeair = dbDecode(table_data)
        density_data = densitas_parasnis(freeair, z)
        table_data.density = density_data
        table_data.save()
    else:
        pass
    return HttpResponseRedirect(request.path_info)

def get_bouger(request,current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    current_density = table_data.density
    current_sba1 = table_data.sba1
    current_sba2 = table_data.sba2
    if current_density is None:
        pass
    elif current_sba1 or current_sba2 is None:
        x, y, z, freeair = dbDecode(table_data)
        sba1_data, sba2_data = bouger(freeair, z, current_density)
        table_data.sba1 = sba1_data
        table_data.sba2 = sba2_data
        table_data.save()
    else:
        pass
    return HttpResponseRedirect(request.path_info)
    