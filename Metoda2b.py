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
               
#ORTOGONALIZCJA Z FILTREM MEDIANOWYM
#zdefiniowanie sygnalu z dwoch elektrod AF8 i AF7 z silnie zarysowanym sygnalem z oka
oko1=dane[14]+dane[13]
#zastosowanie filtru medianowego na powyzszym sygnale
filtr12=sp.medfilt(oko1,21)
#obliczenie wspolczynnika ortagonalizacji
wsp_med=np.dot(dane[12],filtr12)/np.dot(filtr12,filtr12)
#przeprowadzenie procesu ortagonalizacji
FZ_med=dane[12]-(np.dot(dane[12],filtr12)/np.dot(filtr12,filtr12))*filtr12
FZ_med=dane[12]-wsp_med*filtr12#wynik ortogonalizacji z filtrem medianowym

#wyswietlenie sygnalu przed i po filtracji i ortagonalizacji
plt.subplot(211)
plt.title("""Sygnal z elektrody FZ przed i po zastosowaniu
            filtra medianowego i ortagonalizacji""")
plt.ylabel('PRZED')
plt.plot(t[66304:68096],dane[12][66304:68096])
plt.subplot(212)
plt.ylabel('PO')
plt.xlabel('Czas [s]')
plt.plot(t[66304:68096],FZ_med[66304:68096])
plt.show()