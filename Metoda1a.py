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
               
#FILTR MEDIANOWY
filtr1 = sp.medfilt(dane[13],21)
filtr2 = sp.medfilt(dane[14],21)

#wykres porownujacy sygnaly z elektrod AF7 i AF8 przed i po filtracji medianowej
fig, ax = plt.subplots(4)

fig.subplots_adjust(hspace=0)

tytul=np.array(['AF7','FILTR-AF7','AF8','FILTR-AF8'])
ax[0].plot(t[16640:18432],dane[13][16640:18432])
ax[1].plot(t[16640:18432],filtr1[16640:18432])
ax[2].plot(t[16640:18432],dane[14][16640:18432])
ax[3].plot(t[16640:18432],filtr2[16640:18432])
  
ax[0].set_title('Wykres EEG z filtrem')    
plt.setp(ax[:3], xticklabels=[])
plt.show()