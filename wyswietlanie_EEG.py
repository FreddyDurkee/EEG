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

#wykres
f, ax = plt.subplots(15)
f.subplots_adjust(hspace=0)

#zdefiniowanie nazw kanalow
tytul=np.array(['O1','O2','OZ','PO3','PO4','PO7','PO8','CZ','C1','C2','C3','C4','FZ','AF7','AF8'])
  

#zdefiniowanie Slidera
ax_slider = plt.axes([0.125, 0.025, 0.775, 0.03])
slider = plt.Slider(ax_slider,'sekundy',0,(N/fs)-czas,valinit=259,valfmt='%1.0f')


#zdefiniowanie funkcji aktualizujacej dane na Sliderze
def update(val): 
    val=round(val)
    val=int(val)*fs #val w sekundach
    
    ta=t[val:x+val]
           
    for i in range(len(ax)):
        ax[i].clear()
        ax[i].plot(ta,dane[i][val:x+val])
        ax[i].set_yticks([ (max(dane[i][val:x+val])- min(dane[i][val:x+val]))/2 +min(dane[i][val:x+val]) ])
        ax[i].set_yticklabels([tytul[i]])
        
    ax[0].set_title('Wykres EEG')    
    plt.setp(ax[:14], xticklabels=[])
    f.canvas.draw_idle()

slider.on_changed(update)  # aktualizacja danych na podstawie "odczytu" Slidera
update(259)


plt.show()