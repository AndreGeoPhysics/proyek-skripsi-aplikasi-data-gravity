from .models import GravityTable
from scipy import fft
import matplotlib.pyplot as plt
import scipy.interpolate as inter
import math
import json
import numpy as np
from sklearn.linear_model import LinearRegression
from scipy.signal import convolve2d

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

def svd_elkins(input_array):
    matrix_elkins = np.array([[0.00000,-0.0833,0.00000,-0.0833,0.00000],
                              [-0.0833,-0.0667,-0.0334,-0.0667,-0.0833],
                              [0.000000,-0.0334,1.0668,-0.0334,0.00000],
                              [-0.0833,-0.0667,-0.0334,-0.0667,-0.0833],
                              [0.00000,-0.0833,0.00000,-0.0833,0.00000]])
    svdelkins = convolve2d(input_array,matrix_elkins,mode='same',boundary='symm')
    return svdelkins

def svd_rosenbach(input_array):
    matrix_rosenbach = np.array([[0.00000,0.0416,0.00000,0.0416,0.00000],
                                 [0.0416,-0.3332,-0.7500,-0.3332,0.0416],
                                 [0.00000,-0.7500,1.0668,-0.7500,0.0000],
                                 [0.0416,-0.3332,-0.7500,-0.3332,0.0416],
                                 [0.00000,0.0416,0.00000,0.0416,0.00000]])
    svdrosen = convolve2d(input_array,matrix_rosenbach,mode='same',boundary='symm')
    return svdrosen

def svd_henderson(input_array):
    matrix_henderson = np.array([[0.00000,0.0000,-0.0838,0.00000,0.00000],
                                 [0.00000,1.00000,-2.6667,1.00000,0.0000],
                                 [-0.0838,-2.6667,17.000,-2.6667,-0.0838],
                                 [0.0000,1.00000,-2.6667,1.00000,0.00000],
                                 [0.00000,0.00000,-0.0838,0.0000,0.00000]])
    svdhend = convolve2d(input_array,matrix_henderson,mode='same',boundary='symm')
    return svdhend

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
    n3 = n//3*2
    sba_interpolasi = np.array(sba_interpolasi)
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

def get_linear(regional_x1, regional_x2, regional_x3, regional_y1, regional_y2, regional_y3):
    nama_regionalx = [regional_x1,regional_x2,regional_x3]
    nama_regionaly = [regional_y1,regional_y2,regional_y3]
    nama_residualx = [residual_x1,residual_x2,residual_x3]
    nama_residualy = [residual_y1,residual_y2,residual_y3]

    nama_model_regional = ['model_regional1','model_regional2','model_regional3']
    nama_model_residual = ['model_residual1','model_residual2','model_residual3']

    regional_out,residual_out,intercept,gradien = [],[],[],[]

    for i,j,k,l,m,n in zip(nama_regionalx,nama_regionaly,nama_residualx,
                        nama_residualy,nama_model_regional,nama_model_residual):
        m = LinearRegression().fit(i.reshape(-1, 1),j.reshape(-1, 1))
        n = LinearRegression().fit(k.reshape(-1, 1),l.reshape(-1, 1))
        intercept.extend((m.intercept_,n.intercept_))
        gradien.extend((m.coef_,n.coef_))
        y_reg = m.intercept_ + m.coef_ * i
        y_res = n.intercept_ + n.coef_ * k
        regional_out.append(y_reg)
        residual_out.append(y_res)

    for i in range(len(gradien)):
        gradien[i] = gradien[i].flatten()

    #moving average    
    # (c_residual - c_regional)/(m_regional - m_residual)
    x_1 = (intercept[1][0] - intercept[0][0])/(gradien[0][0] - gradien[1][0])
    x_2 = (intercept[3][0] - intercept[2][0])/(gradien[2][0] - gradien[3][0])
    x_3 = (intercept[5][0] - intercept[4][0])/(gradien[4][0] - gradien[5][0])

    X = np.array([x_1, x_2, x_3])
    lamda_x = (2*np.pi)/X
    N = lamda_x/200
    N_mean = np.mean(N)
    return X, N_mean

def movingaverage(input_array, n_mean):
    n = math.floor(n_mean)
    Filter = np.ones([n, n])/n**2
    result = convolve2d(input_array, Filter, mode='same', boundary='symm')
    return result

def fhd(sba_interpolasi):
    fhd_vert = np.array([[-1,0,1],
                        [-1,0,1],
                        [-1,0,1]])
    fhd_hor = np.array([[-1,-1,-1],
                        [0,0,0],
                        [1,1,1]])

    fhd_vert_conv = convolve2d(sba_interpolasi,fhd_vert,mode='same',boundary='symm')
    fhd_hor_conv = convolve2d(sba_interpolasi,fhd_hor,mode='same',boundary='symm')

    FHD = fhd_vert_conv + fhd_hor_conv
    return FHD

def svd(sba_interpolasi):
    elkins = svd_elkins(sba_interpolasi)
    rosenbach = svd_rosenbach(sba_interpolasi)
    henderson = svd_henderson(sba_interpolasi)
    return elkins, rosenbach, henderson
