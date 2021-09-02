import plotly.graph_objects as go
import pandas as pd
import numpy as np
from plotly.offline import plot
from plotly.subplots import make_subplots

df = pd.read_csv('gravity/simpan/22c17709-dbb9-4195-97de-b3f3d8ca427fdata_cimanggung.csv', sep=',')
x = df.iloc[:,0].values.tolist()
y = df.iloc[:,1].values.tolist()
z = df.iloc[:,2].values.tolist()
freeair_anomaly = df.iloc[:,3].values.tolist()
SBA1 = [15.848772773456972, 6.25024621193721, -25.56180497293579, -54.930032970426424, 26.17744667882478, 21.39671383591778, 8.000982931177305, -0.08930788018562907, 27.765093053589524, 29.267888710368837, 18.64201046178036, -9.122099660631847]
SBA2 = [61.996188800000006, 58.173308800000015, 41.83999040000002, 27.25741760000001, 67.1267808, 67.31310400000002, 62.81186880000001, 61.42132800000003, 67.328272, 71.94991680000001, 69.6409696, 57.12456640000002]

fig = make_subplots(rows=4, cols=1)
zdata = [z, freeair_anomaly, SBA1, SBA2]
for n in range(4):
    trace = go.Contour(
            z=[zdata[n]],
            x=x,
            y=y,
            colorscale='viridis',
            )
    fig.append_trace(trace, n+1, 1)

fig.show()