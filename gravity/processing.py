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
    sumbu_x = elevasi /(.04192)
    density = float(konstanta * np.transpose(elevasi).dot(np.linalg.pinv(elevasi.dot(np.transpose(elevasi)))).dot(freeair))
    return sumbu_x, density
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
                                 [0.00000,-0.7500,4.0000,-0.7500,0.0000],
                                 [0.0416,-0.3332,-0.7500,-0.3332,0.0416],
                                 [0.00000,0.0416,0.00000,0.0416,0.00000]])
    svdrosen = convolve2d(input_array,matrix_rosenbach,mode='same',boundary='symm')
    return svdrosen

def svd_henderson(input_array):
    matrix_henderson = np.array([[0.00000,0.0000,-0.0838,0.00000,0.00000],
                                 [0.00000,1.00000,-2.6667,1.00000,0.0000],
                                 [-0.0838,-2.6667,7.0000,-2.6667,-0.0838],
                                 [0.0000,1.00000,-2.6667,1.00000,0.00000],
                                 [0.00000,0.00000,-0.0838,0.0000,0.00000]])
    svdhend = convolve2d(input_array,matrix_henderson,mode='same',boundary='symm')
    return svdhend

def grid(x, y, sba, n):
    ngrid = n 
    x_grid= np.linspace(np.min(x), np.max(x), ngrid)
    y_grid= np.linspace(np.min(y), np.max(y), ngrid)
    x_meshgrid, y_meshgrid = np.meshgrid(x_grid, y_grid)
    interpolasi = inter.Rbf(x, y, sba, method='cubic')
    titik_interpolasi = interpolasi(x_meshgrid, y_meshgrid)
    return x_grid, y_grid, titik_interpolasi

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

def movingaverage(input_array, n):
    Filter = np.ones([n, n])/n**2
    regional = convolve2d(input_array, Filter, mode='same', boundary='symm')
    residual = input_array - regional
    return regional, residual
