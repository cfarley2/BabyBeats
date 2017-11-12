import numpy, pandas, wave, struct
import seqlearn.hmm as seq
import matplotlib.pyplot as plt
from hmmlearn.hmm import GaussianHMM
from pylab import *
from os import listdir
from os.path import isfile, join
from copy import deepcopy


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
    xlabels = []
    ylabels = []
    current = 'Systole'
    for i in range (0, len(df)):
        xlabels.append(df[i])
        if i in s1:
            ylabels.append('S1')
            current = 'Systole'
        elif i in s2:
            ylabels.append('S2')
            current = 'Diastole'
        else:
            ylabels.append(current)
    return xlabels, ylabels

def get_set_a_data():
    mypath = 'set_a/'
    filenames = [f for f in listdir(mypath) if (isfile(join(mypath, f)) and f[-4:] == ".wav")]
    samples = []
    times = []
    
    for file in filenames:
        t, s = get_raw_data(file)
        samples.append(s)
        times.append(t)
        
    return filenames, times, samples

def make_set_a_labels():    
    training_data = get_training_data('set_a_timing.csv')
    training_fnames = list(set(training_data["fname"]))
    s1vals = []
    s2vals = []
    training_xlabels = []
    training_ylabels = []
    training_indices = []
    seq_xlabels = []
    seq_ylabels = []
    seq_lengths = []
    
    
    for fname in training_fnames:
        filtered_by_file = training_data.loc[training_data['fname'] == fname]
        s1 = list(filtered_by_file.loc[filtered_by_file['sound'] == 'S1']['location'])
        s2 = list(filtered_by_file.loc[filtered_by_file['sound'] == 'S2']['location'])
        fname_index = filenames.index(fname[6:])
        training_indices.append(fname_index)
        df = samples[fname_index]
        xlabels, ylabels = generate_training_labels(df, s1, s2)
        
        s1vals.append(s1)
        s2vals.append(s2)
        training_xlabels.append(xlabels)
        training_ylabels.append(ylabels)
        seq_xlabels.extend(xlabels)
        seq_ylabels.extend(ylabels)
        seq_lengths.append(len(df))    
    
    return (s1vals, s2vals, training_xlabels, training_ylabels, training_indices, 
            seq_xlabels, seq_ylabels, seq_lengths)

def plot_waves_with_labels(t,s,s1,s2):
    fig = figure()
    plt.plot(t, s)
    for i in range (0, len(s1)):
        axvline(x = t[s1[i]], color = "red")
    for i in range (0, len(s2)):
        axvline(x = t[s2[i]], color = "green")
        
def HMM_stuff(training_xlabels, training_ylabels):
    X = []
    Y = []
    lengths = []
    for i in range (0,len(training_xlabels)):
        x = numpy.vstack(numpy.array(training_xlabels[i]))
        X.append(x)
        y = numpy.vstack(numpy.array(training_ylabels[i]))
        Y.append(y)
        l = len(training_xlabels[i])
    lengths.append(l)
    
def find_indices_of(array, target):
    indices = []
    for i in range (0, len(array)):
        if array[i] == target:
            indices.append(i)
    return indices

def calculate_percent_correct(predicted, actual):
    total_correct = 0
    for i in range (0, len(predicted)):
        if predicted[i] == actual[i]:
            total_correct = total_correct + 1
    return total_correct/len(predicted)
        

filenames, times, samples = get_set_a_data()
s1vals, s2vals, training_xlabels, training_ylabels, training_indices, seq_xlabels, seq_ylabels, seq_lengths = make_set_a_labels()

for i in range(0,len(training_indices)):
    index = training_indices[i]
    plot_waves_with_labels(times[index], samples[index], s1vals[i], s2vals[i])

modelH = GaussianHMM(n_components=4, covariance_type="diag")
modelH.fit(numpy.vstack(numpy.array(training_xlabels[0])))
resultsH = modelH.predict(numpy.vstack(numpy.array(training_xlabels[0])))

actual_results = deepcopy(training_ylabels[0])
actual_results[actual_results == 'S1'] = 0
actual_results[actual_results == 'Systole'] = 1
actual_results[actual_results == 'S2'] = 2
actual_results[actual_results == 'Diastole'] = 3


modelS = seq.MultinomialHMM()
modelS.fit(numpy.vstack(numpy.array(seq_xlabels)), numpy.vstack(numpy.array(seq_ylabels)), numpy.array(seq_lengths))
resultsS = modelS.predict(numpy.vstack(numpy.array(seq_xlabels)), numpy.array(seq_lengths))

HMM_correct = calculate_percent_correct(resultsH, actual_results)
print("Hmmlearn was", HMM_correct, "percent correct\n")
SEQ_correct = calculate_percent_correct(resultsS, seq_ylabels)
print("Seqlearn was", SEQ_correct, "percent correct\n")

