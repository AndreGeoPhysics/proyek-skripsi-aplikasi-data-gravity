from .models import GravityTable
from scipy import fft
import matplotlib.pyplot as plt
import scipy.interpolate as inter
import json
import numpy as np

def dbDecode(table):
    jsonDec = json.decoder.JSONDecoder()
    x = jsonDec.decode(table.x)
    y = jsonDec.decode(table.y)
    z = jsonDec.decode(table.z)
    freeair = jsonDec.decode(table.freeair)
    return x, y, z, freeair

def densitas_parasnis(freeair, elevasi):
    freeair = np.transpose(np.array([freeair]))
    elevasi = np.transpose(np.array([elevasi]))
    konstanta = 1/(.04192)
    return float(konstanta * np.transpose(elevasi).dot(np.linalg.pinv(elevasi.dot(np.transpose(elevasi)))).dot(freeair))

def bouguer(freeair, elevasi, densitas):
    freeair = np.transpose(np.array([freeair]))
    elevasi = np.transpose(np.array([elevasi]))
    SBA = np.transpose(freeair - (.04192 * float(densitas) * elevasi)).tolist()[0]
    return SBA

def sbagrid(x, y, sba, n):
    ngrid = n 
    x_grid= np.linspace(np.min(x), np.max(x), ngrid)
    y_grid= np.linspace(np.min(y), np.max(y), ngrid)
    x_meshgrid, y_meshgrid = np.meshgrid(x_grid, y_grid)
    interpolasi = inter.Rbf(x, y, sba, method='cubic')
    sba_interpolasi = interpolasi(x_meshgrid, y_meshgrid)
    return x_grid, y_grid, sba_interpolasi

def spectral_analysis(sba_interpolasi, n, sample):
    spec_x = np.arange(1, n+1)
    dt = (n*sample)+sample
    f = (spec_x/2)/dt
    k = 2*np.pi*f
    n1 = n//3
    n2 = n//2
    n3 = n//2*3
    print(n1)
    print(n2)
    print(n3)
    spec_y_1 = sba_interpolasi[:,n1].tolist()
    spec_yfft_1 = abs(fft.fft(spec_y_1))
    lnA_1 = np.log(spec_yfft_1)

    spec_y_2 = sba_interpolasi[n2,:].tolist()
    spec_yfft_2 = abs(fft.fft(spec_y_2))
    lnA_2 = np.log(spec_yfft_2)

    spec_y_3 = sba_interpolasi[:,n3].tolist()
    spec_yfft_3 = abs(fft.fft(spec_y_3))
    lnA_3 = np.log(spec_yfft_3)

    return k, lnA_1, lnA_2, lnA_3