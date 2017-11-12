import numpy, pandas, wave, struct
from pylab import *
from os import listdir
from os.path import isfile, join

def get_raw_data(file):
    FNAME = 'set_a/' + file
    f = wave.open(FNAME)
    frames = f.readframes(-1)
    samples = struct.unpack('h'*f.getnframes(), frames)
    s = list(samples)
    framerate = f.getframerate()
    t = [float(i)/framerate for i in range(len(samples))]
    return (t, s)  

def get_training_data(filename):
    data_frame = pandas.read_csv(filename)
    return data_frame

def generate_training_labels(df, s1, s2):
    labels = []
    for i in range (0, len(df)):
        if i in s1:
            labels.append('S1')
        elif i in s2:
            labels.append('S2')
        else:
            labels.append('none')
    return labels

def get_set_a_data():
    mypath = 'set_a/'
    filenames = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and f[-4:] == ".wav")]
    #filenames = [elem for elem in filenames if elem[-4:] == ".wav"]
    samples = []
    times = []
    
    
    for file in filenames:
        t, s = get_raw_data(file)
        samples.append(s)
        times.append(t)
        
        #fig = figure()
        #plot(t, s)
    return filenames, times, samples

def make_set_a_labels():    
    training_data = get_training_data('set_a_timing.csv')
    training_fnames = list(set(training_data["fname"]))
    s1vals = []
    s2vals = []
    training_labels = []
    
    
    for fname in training_fnames:
        filtered_by_file = training_data.loc[training_data['fname'] == fname]
        s1 = list(filtered_by_file.loc[filtered_by_file['sound'] == 'S1']['location'])
        s1vals.append(s1)
        s2 = list(filtered_by_file.loc[filtered_by_file['sound'] == 'S2']['location'])
        s2vals.append(s2)
        
        fname_index = filenames.index(fname[6:])
        training_labels.append(generate_training_labels(times[fname_index], s1, s2))

filenames, times, samples = get_set_a_data()
make_set_a_labels()

