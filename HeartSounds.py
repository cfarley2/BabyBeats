
# coding: utf-8

# In[ ]:

import wave
import struct
from pylab import *
from os import listdir
from os.path import isfile, join

def plot_waves(file):
    FNAME = 'set_a/' + file
    f = wave.open(FNAME)
    frames = f.readframes(-1)
    print(frames[:20])
    print(f.getsampwidth())
    samples = struct.unpack('h'*f.getnframes(), frames)
    print(samples[:10])
    framerate = f.getframerate()
    t = [float(i)/framerate for i in range(len(samples))]
    print(t[:10])
    fig = figure()
    plot(t, samples)


mypath = 'set_a/'
#print(listdir(mypath))
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
#print(onlyfiles)

for i in range (0,10):
    plot_waves(onlyfiles[i])

"""
for file in onlyfiles:
    plot_waves(file)


print ("blah")
"""

# In[ ]:



