
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
import os
os.chdir('C:\Users\Dominika\Desktop\Projekt_EEG')

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
               
#ORTAGONALIZACJA GRAMA-SCHMIDTA
 
#zdefiniowanie wycikow w czasie sygnalow z elektrod AF8 i FZ
eye2=np.array(dane[14][66304:68096])
eye2_no=np.array(dane[12][66304:68096])

#obliczenie wspolczynnika ortagonalizacji
wsp_ORT=np.dot(eye2_no,eye2)/np.dot(eye2,eye2)

#przeprowadzenie procesu ortagonalizacji
ORT=eye2_no-(wsp_ORT*eye2)

#wyswietlenie sygnalow przed i po ortagonalizacji
plt.subplot(211)
plt.title('Sygnal z elektrody FZ przed i po ortagonalizacji')
plt.ylabel('PRZED')
plt.plot(t[66304:68096],dane[12][66304:68096])
plt.subplot(212)
plt.ylabel('PO')
plt.xlabel('Czas [s]')
plt.plot(t[66304:68096],ORT)

print 'Sprawdzenie ortogonalnosci sygnalow wzgledem siebie', np.dot(eye2,ORT)
plt.show()