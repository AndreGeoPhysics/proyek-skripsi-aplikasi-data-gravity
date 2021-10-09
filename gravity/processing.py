from .models import GravityTable
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
    return float(konstanta * np.transpose(elevasi).dot(np.linalg.pinv(elevasi.dot(np.transpose(elevasi)), hermitian=True)).dot(freeair))

def bouguer(freeair, elevasi, densitas):
    freeair = np.transpose(np.array([freeair]))
    elevasi = np.transpose(np.array([elevasi]))
    SBA = np.transpose(freeair - (.04192 * float(densitas) * elevasi)).tolist()[0]
    return SBA