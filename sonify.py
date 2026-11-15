import pandas as pd #access to al=nalysis library
import numpy as np  #access to math array library & generate sound waves
from scipy.io.wavfile import write #access to scientific computing library

#reads dataset
df = pd.read_csv("GLB.Ts+dssT.csv", skiprows=1)

#Extract annual anomalies
years = df["Year"]
anomalies = pd.to_numeric(df["J-D"],
errors="coerce").dropna()

#normalize anomoly values
min_val = anomalies.min()
max_val = anomalies.max()

#stores pitches
frequencies = []

#repeat for all data points
for value in anomalies:
    norm = (value - min_val) / (max_val - min_val)

    freq = 110*(1760/110)**norm
    #add freq to list
    frequencies.append(freq)  

#sample rate
fs = 44100  

duration_per_note = 0.16

#contains sound sample
audio=[]

#make note for every data point
for freq in frequencies:  
    t=np.linspace(0,duration_per_note,int(fs*duration_per_note),False)
    #soundwave
    tone=(np.sin(2*np.pi*freq*t)
    +0.5*np.sin(2*np.pi*2*freq*t)
    +0.25*np.sin(2*np.pi*3*freq*t))
    audio.extend(tone)

audio=np.array(audio)

#largest mag in audio
max_amp = np.max(np.abs(audio))

if max_amp>0:
    audio=audio/max_amp

print("Frequencies generated:",len(frequencies))

print("Number of years:",len(frequencies))
print("Duration per note:",duration_per_note)
print("Expected length:",len(frequencies)*duration_per_note)

print("NaNs in anomalies:",anomalies.isna().sum())
print("NaNs in audio:",np.isnan(audio).sum())
print("Audio max:",np.max(np.abs(audio)))

print("Number of frequencies:",len(frequencies))
print("Duration per note:",duration_per_note)
print("Audio samples:",len(audio))
print("Expected length (seconds):",len(audio)/fs)

write("sonification.wav",fs,(audio * 32767).astype(np.int16))

print("Done")
print("File saved: sonification.wav")

###     Climate measurments were converted into frequencies
###     and a tone was generated for all the frequencies and
###     attached to an audio arraywith the entire sonification
###     Was then normalized with the use of the max. amplitude
###     and exported as a wav file. 