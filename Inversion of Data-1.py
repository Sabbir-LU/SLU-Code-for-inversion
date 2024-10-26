# -*- coding: utf-8 -*-
"""
Created on Mon Oct 14 08:55:17 2024

@author: ahmed
"""

import pygimli as pg
import pygimli.meshtools as mt
from pygimli.physics import ert
import matplotlib.pyplot as plt

tree = [
    (0.09177, 0.025),
    (0.18082, 0.03205),
    (0.25765, 0.0723),
    (0.30446, 0.15393),
    (0.2918, 0.24626),
    (0.238, 0.32978),
    (0.14746, 0.37853),
    (0.03616, 0.39077),
    (-0.06002, 0.35599),
    (-0.1314, 0.28747),
    (-0.15695, 0.20214),
    (-0.13594, 0.12438),
    (-0.08431, 0.06175),
    (0.00495, 0.025)
]

refinement = [    
    [0.09035, 0.061],
    [0.17058, 0.06735],
    [0.23189, 0.09974],
    [0.26712, 0.16119],
    [0.25722, 0.23347],
    [0.21276, 0.30248],
    [0.13656, 0.34351],
    [0.04054, 0.35407],
    [-0.0406, 0.32473],
    [-0.09963, 0.26807],
    [-0.11952, 0.20163],
    [-0.10321, 0.14128],
    [-0.06227, 0.09161],
    [0.01207, 0.061]
]

data = ert.load('D:/SLU/Data/TREE_dipole_normal_1.udf', verbose=True)
print(data)

plc = mt.createPolygon(tree, isClosed=True, addNodes=10, interpolate='spline')

for j in data.sensors():
    plc.createNode(j, marker = -99)

for k in refinement:
    plc.createNode(k)

ax, cb = pg.show(plc)

mesh = mt.createMesh(plc)
print(mesh)

ax, cb = pg.show(mesh)

for i, s in enumerate(data.sensors()):
    ax.text(s.x(), s.y(), f"{i+1}", zorder=100, color='blue')

pg.wait()


data["k"] = ert.createGeometricFactors(data, mesh=mesh, numerical=True)
data["rhoa"] = data["r"] * data["k"]
ax, cb = ert.show(data, "rhoa", circular=True)

data.set('err', ert.estimateError(data))


#IP
mgr = ert.ERTIPManager(data)
mgr.invert(mesh=mesh, verbose=True)
ax, cb = mgr.showIPModel(cMin=4, cMax=7, coverage=1)

'''
#ERT
mgr2 = ert.Manager(data)
mgr2.invert(mesh=mesh, verbose=True)
ax, cb = mgr2.showResult(cMin=100, cMax=500, coverage=1)
'''