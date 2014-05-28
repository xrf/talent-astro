#!/usr/bin/env python
import math, os, subprocess, sys
import numpy as np
import matplotlib.pyplot as plt

# type DataFrame a = ([String], Map String [a])

FNULL = open(os.devnull, 'w')

def df_read(filename):
    data = []
    with open(filename) as f:
        for line in f:
            data.append(line.split())
    header = data[0]
    data = data[1:]
    data = [list(map(float, row)) for row in data]
    data = np.transpose(np.array(data))
    cols = {name: data[i] for i, name in enumerate(header)}
    return header, cols

def df_plot(df, x=0, ys=None, y_label=None, title=None, filename=None,
            log_x=False, log_y=False, x_range=None, y_range=None):
    colnames, cols = df
    if type(x) == int:
        x = colnames[x]
    ys = list(ys or colnames[1:])
    for y in ys:
        if type(y) == int:
            y = colnames[y]
        plt.plot(cols[x], cols[y], label=y)
    box = plt.axes().get_position()
    plt.axes().set_position([box.x0, box.y0, box.width * 0.8, box.height])
    plt.axes().set_xlabel(x)
    if y_label is not None:
        plt.axes().set_ylabel(y_label)
    if title is not None:
        plt.axes().set_title(title)
    if log_x:
        plt.axes().set_xscale("log")
    if log_y:
        plt.axes().set_yscale("log")
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    if x_range is not None:
        plt.xlim(x_range)
    if y_range is not None:
        plt.ylim(y_range)
    if filename is None:
        plt.show()
    else:
        plt.savefig(filename)
    plt.clf()


def run_xnet(temperature=5, stop_time=100, cols=None, tag="", override_filename=None):
    with open("th_constant", "w") as f:
        f.write('''
Flat Profile at {0} GK
 0.000000E+00     Start Time  
 {1}     Stop Time
 1.000000E-12     Init Del t
0.000000e+00 {0} 1.000000E+06
{1} {0} 1.000000E+06
        '''.strip().format(temperature, stop_time))
    subprocess.check_call(["source/xnet"], stdout=FNULL)
    df = df_read("ev1")
    default_filename="ev1{}_{:010.5f}".format(tag, temperature)
    df_plot(df, x=1, ys=cols or df[0][6:-1], title="{}GK".format(temperature),
            y_range=[1e-16, 1],
            filename="../../../" + (override_filename or default_filename) + ".png",
            log_x=True, log_y=True)


'''
 he4   c12   o16  ne20  mg24  si28   s32  ar36  ca40  ti44
cr48  fe52  ni56  zn60
'''
#Time = 1
#Temperature = 2
#Density = 3
#dE/dt = 4
#Nuclei = [6:-1]
os.chdir("xnet_public/branches/public")

#.0658
# run_xnet(.1, 1e17, override_filename="out",
#             cols=["ni56", "si28", "s32", "o16", "mg24", "c12"])
# sys.exit()


T = .1
time_factor = 1e17
time_exponent = 0
while T < 6.:
    stop_time = time_factor * math.exp(time_exponent * (5. - T))
    print(T, stop_time)
    # C  -> Mg   < 0.81GK
    # O  -> S    < 
    # Si -> Ni   < 1.58GK
    run_xnet(T, stop_time,
             cols=["ni56", "si28", "s32", "o16", "mg24", "c12"])
    T *= 1.03
