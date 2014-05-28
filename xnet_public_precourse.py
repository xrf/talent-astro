#!/usr/bin/env python
import numpy as np
import matplotlib.pyplot as plt

data = []
'''
k
Time
T(GK)
Density
dE/dt
Timestep
he4
c12
o16
ne20
mg24
si28
s32
ar36
ca40
ti44
cr48
fe52
ni56
zn60
It
'''
with open("xnet_public/branches/public/ev1") as f:
    for line in f:
        data.append(line.split())

header = data[0]
data = data[1:]
data = [map(float, row) for row in data]
data = np.transpose(np.array(data))
data = {name: data[i] for i, name in enumerate(header)}

x = data["Time"]
cols='''
he4
c12
o16
ne20
mg24
si28
s32
ar36
ca40
ti44
cr48
fe52
ni56
zn60
'''.strip().split()
ys = ((name, data[name]) for name in cols)
for name, y in ys:
    plt.plot(x, y, label=name)
box = plt.axes().get_position()
plt.axes().set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.axes().set_title("Plot")
plt.axes().set_xscale("log")
plt.axes().set_yscale("log")
plt.axes().set_xlabel("time")
plt.axes().set_ylabel("mass fraction")
plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
plt.show()
