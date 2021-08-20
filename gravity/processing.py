from .models import InputModel, GravityTable
import json
import numpy as np
import scipy.interpolate as interpolate
import utm

def dbDecode():
    jsonDec = json.decoder.JSONDecoder()
    x = jsonDec.decode(GravityTable.x)
    y = jsonDec.decode(GravityTable.y)
    z = jsonDec.decode(GravityTable.z)
    FA = jsonDec.decode(GravityTable.FA)

def densitas_parasnis(freeair, elevasi):
    freeair = np.transpose(np.array([freeair]))
    elevasi = np.transpose(np.array([elevasi]))
    konstanta = 1/(.04192)
    return float(konstanta * np.transpose(elevasi).dot(np.linalg.pinv(elevasi.dot(np.transpose(elevasi)), hermitian=True)).dot(freeair))

def bouger(freeair, elevasi, densitas):
    freeair = np.transpose(np.array([freeair]))
    elevasi = np.transpose(np.array([elevasi]))
    SBA1 = np.transpose(freeair - (.04192 * densitas * elevasi)).tolist()[0]
    SBA2 = np.transpose(freeair - (.04192 * 1.89 * elevasi)).tolist()[0]
    return SBA1, SBA2

