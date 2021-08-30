from .models import GravityTable
import json
import numpy as np
import scipy.interpolate as interpolate
import utm
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import base64
from io import BytesIO


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
    return float(konstanta * np.transpose(elevasi).dot(np.linalg.pinv(elevasi.dot(np.transpose(elevasi)), hermitian=True)).dot(freeair))

def bouger(freeair, elevasi, densitas):
    freeair = np.transpose(np.array([freeair]))
    elevasi = np.transpose(np.array([elevasi]))
    SBA1 = np.transpose(freeair - (.04192 * float(densitas) * elevasi)).tolist()[0]
    SBA2 = np.transpose(freeair - (.04192 * 1.89 * elevasi)).tolist()[0]
    return SBA1, SBA2

def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def processing_data(x, y, z, densitas, SBA1, SBA2, wilayah):
    class kontur:
        def __init__(self,x,y,z):
            self.x = x
            self.y = y
            self.z = z

        def get_minmax(self):
            return min(self.x), max(self.x), min(self.y), max(self.y)

        def meshgrid(self, window_x, window_y, x_min = 'data', x_max='data', y_min='data', y_max='data'):
            if x_min == 'data' and x_max == 'data' and y_min == 'data' and y_max == 'data': 
                x_min, x_max, y_min, y_max = kontur.get_minmax(self)
            x_grid  = np.arange(x_min, x_max, window_x)
            y_grid  = np.arange(y_min, y_max, window_y)
            return np.meshgrid(x_grid, y_grid)
    
        def get_grid(self, window_x, window_y, meshgrid=None, x_min = 'data', x_max='data', y_min='data', y_max='data',metode='linear'):
            if meshgrid is None:
                x_grid, y_grid  = kontur.meshgrid(self, window_x, window_y, x_min, x_max, y_min, y_max)
            elif not meshgrid is None:
                x_grid, y_grid  = meshgrid
            x, y, z         = self.x, self.y, self.z
            result = interpolate.griddata((x,y), z, (x_grid, y_grid), method=metode)
            return result

    window = 1200
    grid_freeair = kontur(x,y,freeair_anomaly)
    xi,yi        = grid_freeair.meshgrid(window_x=window, window_y=window)
    grid_fa      = grid_freeair.get_grid(meshgrid=(xi,yi), window_x=window, window_y=window, metode='nearest')
    grid_dem     = kontur(x,y,z).get_grid(meshgrid=(xi,yi), window_x=window, window_y=window, metode='nearest')
    grid_sba1     = kontur(x,y,SBA1).get_grid(meshgrid=(xi,yi), window_x=window, window_y=window, metode='nearest')
    grid_sba2     = kontur(x,y,SBA2).get_grid(meshgrid=(xi,yi), window_x=window, window_y=window, metode='nearest')
    
    # Analisis dan Interpretasi

    def moving_average_2d(grid, window):
        window = np.ones((window[0],window[1]))
        window /= window.sum()
        return convolve2d(grid, window, mode='same', boundary='symm')

    def svd(grid,mode='elkins'):
        mode = mode.casefold()
        if mode == 'elkins':
            matriks = np.array([[ 0.00,    -0.0833,   0.00,   -0.0833,  0.00  ],
                                [-0.083,   -0.066,   -0.0334, -0.0667, -0.0833],
                                [ 0.00,    -0.0334,   1.0668, -0.0334,  0.00  ],
                                [-0.0833,  -0.0667,  -0.0334, -0.0667, -0.0833],
                                [ 0.00,    -0.0833,   0.00,   -0.0833,  0.00  ]])
        elif mode == 'rosenbach': 
            matriks = np.array([[ 0.00,    -0.0416,   0.00,   -0.0416,  0.00  ],
                                [-0.0416,  -0.3332,  -0.75,   -0.3332, -0.0416],
                                [ 0.00,    -0.75,     4.00,   -0.75,    0.00  ],
                                [-0.0416,  -0.3332,  -0.75,   -0.3332, -0.0416],
                                [ 0.0,     -0.0416,   0.00,   -0.0416,  0.00  ]])
        return convolve2d(grid, matriks, mode='same', boundary='symm')


    svd_elkins_sba1 = svd(grid_sba1)
    svd_elkins_sba2 = svd(grid_sba2)
    svd_rosenb_sba1 = svd(grid_sba1,mode='rosenbach')
    svd_rosenb_sba2 = svd(grid_sba2,mode='rosenbach')

    # Ploting

    grids = [grid_fa, grid_dem, grid_sba1, grid_sba2]
    judul = ['Freeair Anomaly %.2f'%(wilayah),'Elevasi %.2f'%(wilayah), 'SBA Kawah Ijen\n dengan densitas %.2f'%(densitas),'SBA Kawah Ijen\n dengan densitas %.2f'%(1.89)]

    plt.switch_backend('AGG')
    plt.figure()
    for i in range(len(grids)):
        plt.subplot(2,2,i+1)
        plt.title(judul[i], fontweight = 'bold')
        plt.contourf(xi, yi , grids[i], levels=50, cmap='nipy_spectral')
        plt.xlabel('Easting')
        plt.ylabel('Northing')
        plt.colorbar()
        plt.tight_layout(pad=0.3, w_pad=0.8, h_pad=0.8)

    grids = [svd_elkins_sba1, svd_elkins_sba2, svd_rosenb_sba1, svd_rosenb_sba2]
    judul = ['Elkins SBA\ndengan densitas %.2f'%(densitas), 'Elkins SBA\ndengan densitas %.2f'%(1.89),
             'Rosenbach SBA\ndengan densitas %.2f'%(densitas), 'Rosenbach SBA\ndengan densitas %.2f'%(1.89)]

    plt.figure()
    for i in range(len(grids)):
        plt.subplot(2,2,i+1)
        plt.title(judul[i], fontweight = 'bold')
        plt.contourf(xi, yi , grids[i], levels=50, cmap='nipy_spectral')
        plt.xlabel('Easting')
        plt.ylabel('Northing')
        plt.colorbar()
        plt.tight_layout(pad=0.3, w_pad=0.4, h_pad=0.4)
    graph = get_graph()
    return graph