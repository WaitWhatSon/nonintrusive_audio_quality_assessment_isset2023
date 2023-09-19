# generate dataset .pkl

import pandas as pd
from os import listdir
from os.path import isfile, join

import sys

import numpy as np 

import librosa
import pickle

import h5py

def min_max_normalise(values):
    _min, _max = np.min(values), np.max(values)
    return (values - _min) / (_max - _min)

def mos_normalise(values):
    return (values - 1) / 4


def main(args):
    
    data_csv = args[0]
    
    ref_dir = args[1]
    deg_dir = args[2]
    
    dataset_file_name = args[3]
    
    df = pd.read_csv(data_csv)
    # df.hist(column = ["moslqo"], bins = 5)
    

    ref_ = ("000" + df.reference.astype(int).astype(str)).str[-3:]
    ref_s = ref_dir + ref_ + ".wav"

    deg_s = deg_dir + ref_ + "_" + df.degraded + ".wav"

    df.reference = ref_s
    df.degraded = deg_s

    df.to_csv("dataset_250_refs.csv", index=False)
    
    #######  
    
    # df = pd.read_csv("dataset_250_refs.csv")
    
    
    inputs = []
    outputs = []
    refnums = []

    TIME = 10
    SR = 48000
    N_FFT = 2048
    HOP_LENGTH = 256
    N_MELS = 256

    for i, row in df.iterrows():
        filename = row.degraded
        # loading and cutting
        audio, _ = librosa.load(filename, sr=SR)
        audio = audio[:TIME * SR]
        # mel spectrograms
        spectrogram = librosa.feature.melspectrogram(y=audio, sr=SR, n_fft=N_FFT, hop_length=HOP_LENGTH, n_mels=N_MELS)
        spectrogram = librosa.power_to_db(spectrogram, ref=np.max)
        spectrogram = np.rot90(spectrogram)
        # normalisation
        spectrogram = min_max_normalise(spectrogram)
        mos = mos_normalise(row.moslqo)
    
        inputs.append(spectrogram)
        outputs.append(mos)
        
        refnums.append(filename.split('\\')[-1].split('_')[0])
    
        print(f'{i + 1} of {len(df)} processed', end='\r')

    inputs = np.array(inputs)
    outputs = np.array(outputs)
    refnums = np.array(refnums)
    
    print("inputs shape: ", np.shape(inputs))


    # save as pickle
    with open(dataset_file_name + '.pkl', 'wb') as file:
        pickle.dump((inputs, outputs, refnums), file)
    
    
    try: 
        # file test
        temp = np.load(dataset_file_name +".pkl", allow_pickle=True)

        inputs_pickle = temp[0]
        outputs_pickle = temp[1]
        refnums_pickle = temp[2]

        print("PICLKE FILE TEST")
        print("INPUTS SHAPE ", np.shape(inputs_pickle))
        print("OUTPUTS SHAPE ", np.shape(outputs_pickle))
        print("REFNUMS SHAPE ", np.shape(refnums_pickle))
        
        print("pickle file ok")

    except:
        print("cannot open pickle file")

    
    # save as hdf5

    with h5py.File(dataset_file_name + '.hdf5', 'w') as f:
        f.create_dataset('test_x', data = inputs)
        f.create_dataset('test_y', data = outputs)
        f.create_dataset('test_refnum', data = refnums)
        
    print("hdf5 file saved")
        
    
if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))