from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect
from .forms import FileForm, GridForm
from .models import GravityTable, GridTable
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .processing import *
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
import os
import json
import pandas as pd

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

@login_required(login_url=settings.LOGIN_URL)
def get_topo(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    x, y, z, freeair = dbDecode(table_data)
    topo_data = {}
    topo_data['x'] = x
    topo_data['y'] = y
    topo_data['z'] = z
    topo_data['freeair'] = freeair
    return JsonResponse(topo_data)

@login_required(login_url=settings.LOGIN_URL)
def get_bouguer(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    x, y, z, freeair = dbDecode(table_data)
    current_density = table_data.density
    current_sba = table_data.sba
    if current_density is None:
        density_data = densitas_parasnis(freeair, z)
        sba_data = bouguer(freeair, z, density_data)
        table_data.density = density_data
        table_data.sba =  sba_data
        table_data.save()
    elif current_sba is None:
        sba_data = bouguer(freeair, z, current_density)
        table_data.sba = sba_data
        table_data.save()
    else:
        sba_data = current_sba
    sba_dict = {}
    sba_dict['sba'] = sba_data
    return JsonResponse(sba_dict)

@login_required(login_url=settings.LOGIN_URL)
def save_grid(request, current_id):
    if request.method == 'POST':
        form = GridForm(request.POST)
        if form.is_valid():
            ngrid = request.POST['ngrid']
            sample_interval = int(request.POST['sample_interval'])
            gravity_data = GravityTable.objects.get(unique_id=current_id)
            grid_data = GridTable(grid_ref=gravity_data, n_grid=ngrid, sample=sample_interval)
            grid_data.save()
            pesan = "Input berhasil disimpan!"
            konteks = {
            'form' : form,
            'pesan' : pesan,
            'current_id' : current_id,
            }
            return render(request, 'save-grid.html', konteks)
    else:  
        form = GridForm()
        konteks = {
            'form': form,
            'current_id' : current_id,
        }
    return render(request, 'save-grid.html', konteks)

@login_required(login_url=settings.LOGIN_URL)
def bouguer_map(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    jsonDec = json.decoder.JSONDecoder()
    sba = jsonDec.decode(table_data.sba)
    n = grid_data.n_grid
    print(n)
    x_grid, y_grid, sba_grid = sbagrid(x, y, sba, n)
    grid_data.x_grid = x_grid 
    grid_data.y_grid = y_grid
    grid_data.sba_interpolate = sba_grid
    grid_data.save()
    sbagrid_dict = {}
    sbagrid_dict['sbagrid'] = json.dumps(sba_grid.tolist())
    sbagrid_dict['xgrid'] = json.dumps(x_grid.tolist())
    sbagrid_dict['ygrid'] = json.dumps(y_grid.tolist())
    return JsonResponse(sbagrid_dict)
 
def bouguer_map(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    jsonDec = json.decoder.JSONDecoder()
    sba = jsonDec.decode(table_data.sba)
    n = grid_data.n_grid
    print(n)
    x_grid, y_grid, sba_grid = sbagrid(x, y, sba, n)
    grid_data.x_grid = x_grid 
    grid_data.y_grid = y_grid
    grid_data.sba_interpolate = sba_grid
    grid_data.save()
    sbagrid_dict = {}
    sbagrid_dict['sbagrid'] = json.dumps(sba_grid.tolist())
    sbagrid_dict['xgrid'] = json.dumps(x_grid.tolist())
    sbagrid_dict['ygrid'] = json.dumps(y_grid.tolist())
    return JsonResponse(sbagrid_dict)

def get_spectrum(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    jsonDec = json.decoder.JSONDecoder()
    sba_interpolasi = grid_data.sba_interpolate
    n = grid_data.n_grid
    sample = grid_data.sample
    k, lnA_1, lnA_2, lnA_3 = spectral_analysis(sba_interpolasi, n, sample)
    grid_data.k = k 
    grid_data.lnA_1 = lnA_1
    grid_data.lnA_2 = lnA_2
    grid_data.lnA_3 = lnA_3
    grid_data.save()
    n_half = n//2
    print(n_half)
    spectrum_dict = {}
    spectrum_dict['k'] = json.dumps(k[:n_half].tolist())
    spectrum_dict['lnA_1'] = json.dumps(lnA_1[:n_half].tolist())
    spectrum_dict['lnA_2'] = json.dumps(lnA_2[:n_half].tolist())
    spectrum_dict['lnA_3'] = json.dumps(lnA_3[:n_half].tolist())
    return JsonResponse(spectrum_dict)

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
def testing(request):
    return render(request, 'testing.html')

@login_required(login_url=settings.LOGIN_URL)
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            nama_user = request.user
            print(nama_user)
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