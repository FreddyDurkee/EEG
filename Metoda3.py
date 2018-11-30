# -*- coding: utf-8 -*-
#PROJEKT EEG
#AUTORZY: Dominika Wójcik, Lija Rubajczyk
#KIERUNEK: INZYNIERIA BIOMEDYCZNA
#DATA ZDANIA PROJEKTU: 18.01.2016

#EEG.py

#importowanie niezbednych modulow
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mne
import os
import scipy.signal as sp

#przygotowanie danych

#zmiana lokalizacji
x=raw_input('Podaj lokalizacje folderu z plikami: ')
os.chdir(x)

#wczytanie sygnalu za pomoca modulu h5py
sygnal=h5py.File("RecordSession_2005.01.01_01.18.03.hdf5")
data=sygnal["RawData"]
samples=np.array(data["Samples"])
sample=samples.T

#zdefiniowanie podstawowych parametrow
czas=7
N=91402
fs=256.
t=np.arange(0,N/fs,1./fs)
x=fs*czas

#zdefiniowanie macierzy z sygnalami z poszczegolnych kanalow
dane=np.array([sample[4][768:],sample[2][768:],
               sample[3][768:],sample[5][768:],
               sample[1][768:],sample[6][768:],
               sample[0][768:],sample[7][768:],
               sample[14][768:],sample[11][768:],
               sample[12][768:],sample[9][768:],
               sample[8][768:],sample[13][768:],
               sample[10][768:]]) 
               
#WYKRYWANIE EOG AUTOMATYCZNIE
#numer kanalu zdefiniowany przez uzytkownika
i=input('Podaj numer kanalu z przedzialu 0-14: ')
#zdefiniowanie rodzajow kanalow i ich nazw
ch_types = ['eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eeg','eog']
ch_names = ['O1','O2','OZ','PO3','PO4','PO7','PO8','CZ','C1','C2','C3','C4','FZ','AF7','AF8']

#stworzenie macierzy z parametrami pomiarowymi
info = mne.create_info(ch_names=ch_names,sfreq=fs, ch_types=ch_types)

#stworzenie macierzy zawierajacej dane i parametry
raw = mne.io.RawArray(dane, info)

#wyszukiwanie artefaktow EOG
event_id=998
eog_events = mne.preprocessing.find_eog_events(raw, event_id)
picks = mne.pick_types(raw.info, meg=False, eeg=True, stim=False, eog=True, exclude='bads')

tmin,tmax=-2.0,2.0 #zefiniowanie przedzialu wydarzen
epochs = mne.Epochs(raw, eog_events, event_id, tmin,tmax,picks=picks)
data = epochs.get_data()

print("Ilosc wykrytych artefaktow EOG: %d" % len(data))

#wyodrebnienie kolumny z macierzy 3D do macierzy 1D
def column(matrix, i):
    return [row[i] for row in matrix]
eog_indexes=column(np.squeeze(data).T,i)
                  
#wyswietlenie artefaktow nalozonych na siebie
plt.plot(1e3 * epochs.times, eog_indexes)
plt.xlabel('Times (ms)')
plt.ylabel('EOG (muV)')
plt.show()
