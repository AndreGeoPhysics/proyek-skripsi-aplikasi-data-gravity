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

def gravitymodelbuilder(nama_user, nama, df, ngrid, sample_interval):
    user_id = nama_user
    nama_proyek = nama
    x = json.dumps(df.iloc[:,0].values.tolist())
    y = json.dumps(df.iloc[:,1].values.tolist())
    z = json.dumps(df.iloc[:,2].values.tolist())
    freeair = json.dumps(df.iloc[:,3].values.tolist())
    data = GravityTable(user_id=user_id, nama_proyek=nama_proyek, x=x, y=y, z=z, freeair=freeair)
    data.save()
    grid_data = GridTable(grid_ref=data, n_grid=ngrid, sample=sample_interval)
    grid_data.save()
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
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    n = grid_data.n_grid
    x_grid, y_grid, z_grid = grid(x, y, z, n)
    x_grid, y_grid, fa_grid = grid(x, y, freeair, n)
    grid_data.x_grid = x_grid 
    grid_data.y_grid = y_grid
    grid_data.z_interpolate = z_grid
    grid_data.fa_interpolate = fa_grid
    grid_data.save()
    topo_data = {}
    topo_data['x'] = x
    topo_data['y'] = y
    topo_data['z'] = z
    topo_data['freeair'] = freeair
    topo_data['x_grid'] = json.dumps(x_grid.tolist())
    topo_data['y_grid'] = json.dumps(y_grid.tolist())
    topo_data['z_grid'] = json.dumps(z_grid.tolist())
    topo_data['fa_grid'] = json.dumps(fa_grid.tolist())
    return JsonResponse(topo_data)

@login_required(login_url=settings.LOGIN_URL)
def get_bouguer(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    x, y, z, freeair = dbDecode(table_data)
    density_data = densitas_parasnis(freeair, z)
    sba_data = bouguer(freeair, z, density_data)
    table_data.density = density_data
    table_data.sba =  sba_data
    table_data.save()
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
            grid_data = GridTable.objects.get(grid_ref=gravity_data)
            grid_data.n_grid = ngrid
            grid_data.sample = sample_interval
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
    x_grid, y_grid, sba_grid = grid(x, y, sba, n)
    grid_data.x_grid = x_grid 
    grid_data.y_grid = y_grid
    grid_data.sba_interpolate = json.dumps(sba_grid.tolist())
    grid_data.save()
    sbagrid_dict = {}
    sbagrid_dict['sbagrid'] = json.dumps(sba_grid.tolist())
    return JsonResponse(sbagrid_dict)
 
def get_fhd(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    jsonDec = json.decoder.JSONDecoder()
    sba_interpolasi = jsonDec.decode(grid_data.sba_interpolate)
    FHD = fhd(sba_interpolasi)
    fhd_dict = {}
    fhd_dict['fhd'] = json.dumps(FHD.tolist())
    return JsonResponse(fhd_dict)

def get_svd(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    jsonDec = json.decoder.JSONDecoder()
    sba_interpolasi = jsonDec.decode(grid_data.sba_interpolate)
    elkins, rosenbach, henderson = svd(sba_interpolasi)
    svd_dict = {}
    svd_dict['elkins'] = json.dumps(elkins.tolist())
    svd_dict['rosenbach'] = json.dumps(rosenbach.tolist())
    svd_dict['henderson'] = json.dumps(henderson.tolist())
    return JsonResponse(svd_dict)

def get_gauss(request, current_id):
    table_data = GravityTable.objects.get(unique_id=current_id)
    grid_data = GridTable.objects.get(grid_ref=table_data)
    x, y, z, freeair = dbDecode(table_data)
    jsonDec = json.decoder.JSONDecoder()
    sba_interpolasi = jsonDec.decode(grid_data.sba_interpolate)
    gauss = gaussian(sba_interpolasi)
    gauss_dict = {}
    gauss_dict['gauss'] = json.dumps(gauss.tolist())
    return JsonResponse(gauss_dict)

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
    grid_data = GridTable.objects.get(grid_ref=work_data)
    konteks = {
        'work_data' : work_data,
        'grid_data' :  grid_data,
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
            ngrid = request.POST['ngrid']
            sample_interval = request.POST['sample_interval']
            uploaded_data = request.FILES['file_gravity']
            file_df, check, pesan = handle_file(uploaded_data, delim)
            if check == True:
                model_id = gravitymodelbuilder(nama_user, nama, file_df, ngrid, sample_interval)
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


# def get_spectrum(request, current_id):
#     table_data = GravityTable.objects.get(unique_id=current_id)
#     grid_data = GridTable.objects.get(grid_ref=table_data)
#     x, y, z, freeair = dbDecode(table_data)
#     jsonDec = json.decoder.JSONDecoder()
#     sba_interpolasi = jsonDec.decode(grid_data.sba_interpolate)
#     n = grid_data.n_grid
#     sample = grid_data.sample
#     k, lnA_1, lnA_2, lnA_3 = spectral_analysis(sba_interpolasi, n, sample)
#     spectral_data = SpectralTable(spectral_ref=grid_data, k=k, lnA_1=lnA_1, lnA_2=lnA_2, lnA_3=lnA_3)
#     spectral_data.save()
#     n_half = n//2
#     spectrum_dict = {}
#     spectrum_dict['k'] = json.dumps(k[:n_half].tolist())
#     spectrum_dict['lnA_1'] = json.dumps(lnA_1[:n_half].tolist())
#     spectrum_dict['lnA_2'] = json.dumps(lnA_2[:n_half].tolist())
#     spectrum_dict['lnA_3'] = json.dumps(lnA_3[:n_half].tolist())
#     return JsonResponse(spectrum_dict)
