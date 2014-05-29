#!/usr/bin/env python
import glob, math, os, re, shutil, subprocess, sys, time
import numpy as np
import dataframe as df

def read_file(filename):
    with open(filename) as f:
        return f.read()

def write_file(filename, s):
    with open(filename, "w") as f:
        f.write(s)

FNULL = open(os.devnull, 'w')

use_gravity = False
prefix = "Sedov"
num_cycles = 100#4500
t_end = 9.9e19
t_print = t_end
t_movie = t_end
n_print = 10

x_count = 100
x_min = 0.
x_max = 1.
dx = (x_max - x_min) / x_count

gamma = 5. / 3.
density = 1
pressure = 1e-3
blast_energy = 10.
blast_radius = dx
blast_pressure = blast_energy / (4. * math.pi / 3. * blast_radius ** 3) * (gamma - 1.)
assert abs(blast_pressure - 1.59e6) < 0.01e6

if use_gravity:
    potential = "-1. / xf(n) ** 2"
else:
    potential = "0."

s = read_file("VH1/src/PPMLR/forces.f90")
# note: need to find a way to interpret '\10' as '\1' + '0'
s = re.sub(r"^([\t ]*grav *\( *n *\) *=)[^\n]*$",
           r"\1 " + potential.replace("\\", "\\\\"),
           s, flags=re.MULTILINE)
write_file("VH1/src/PPMLR/forces.f90", s)

os.chdir("VH1/src/Starter")
write_file("vhone.f90", read_file("../../../ex2-vhone.f90").format(**locals()))
write_file("../../indat", '''
&hinput
 rstrt   = 'no'
 prefix  = '{prefix}'
 ncycend = {num_cycles}
 ndump   = 5000000
 nprin   = {n_print}
 nmovie  = 1000000
 endtime = {t_end}
 tprin   = {t_print}
 tmovie  = {t_movie} /
'''.strip().format(**locals()) + "\n")
subprocess.check_call(["make"], stdout=FNULL)
os.chdir("../../..")

os.chdir("VH1")
try:
    shutil.rmtree("output")
except:
    pass
os.mkdir("output")
subprocess.check_call(["./vh1-starter"])
os.chdir("..")

r = re.compile("^Wrote +{prefix}([0-9]+) +to disk at time ="
               .format(prefix=re.escape(prefix)) +
               " *([-+.0-9eE]+) *\(ncycle = *[0-9]+ *\)$")
time_map = {1000: 0}
with open("VH1/output/{prefix}.hst".format(prefix=prefix)) as f:
    for line in f:
        m = r.match(line.strip())
        if m:
            index, time = m.groups()
            time_map[int(index)] = float(time)
try:
    for i in range(1000, 9999):
        data = df.DataFrame()
        data.read("VH1/output/{prefix}{index}.dat".format(prefix=prefix, index=i),
                  with_header=False)
        cols = ["time", "density", "pressure", "velocity"]
        data.remap_names({str(k): v for k, v in enumerate(cols)})
        data.plot(
            filename="VH1/output/{prefix}{index}.png".format(prefix=prefix, index=i),
            title="time = {}".format(time_map[i]),
            #ys=[1],
            y_range=(0, 5),
        )
except OSError:
    pass
print("# of frames = {}".format(i - 999))
