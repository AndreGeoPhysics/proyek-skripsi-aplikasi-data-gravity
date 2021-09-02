from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import FileForm
from .models import GravityTable
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .processing import *
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import os
import json
import pandas as pd


@login_required(login_url=settings.LOGIN_URL)
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

@login_required(login_url=settings.LOGIN_URL)
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

@login_required(login_url=settings.LOGIN_URL)
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

@login_required(login_url=settings.LOGIN_URL)
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
    return redirect(request.path)

@login_required(login_url=settings.LOGIN_URL)
def get_bouger(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    current_density = table_data.density
    current_sba = table_data.sba
    if current_density is None:
        pass
    elif current_sba is None:
        x, y, z, freeair = dbDecode(table_data)
        sba_data = bouger(freeair, z, current_density)
        table_data.sba = sba_data
        table_data.save()
    else:
        pass
    return redirect(request.path)

def plot_data(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    x, y, z, freeair_anomaly = dbDecode(table_data)
    densitas = table_data.density
    SBA = table_data.sba
    wilayah = table_data.nama_proyek
    fig = go.Figure()
    contour = go.Contour(
              z=z,
              x=x,
              y=y,
              colorscale='viridis',
              )
    fig.add_trace(contour)
    plt_div = plot(fig, output_type='div')   
    return render(request, "plot-data.html", context={'plt_div': plt_div})
    
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
    konteks = {
        'work_data' : work_data,
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
