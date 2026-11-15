import pandas as pd 
import numpy as np
from scipy.io.wavfile import write

#read dataset
#sepr"\s+" tells pandas the columns are separated by spaces

df = pd.read_csv("GMSL_extrap_1993_2050.2026_02_05.txt",skiprows=47,sep=r"\s+",header=None)

#column names
df.columns=["Time","SeaLevel","Rate","ExtrapolatedFit","ExtrapolatedRate","QuadraticFit"]

#get sea level measurments
values=pd.to_numeric(
    df["SeaLevel"],errors="coerce")

#remove missing value code (99900)
values=values[values !=99900]

#remove and NaN values (in case)
values=values.dropna()
values=values[::10]

print("Measurments after downsampling:",len(values))

#data range
min_val=values.min()
max_val=values.max()

#convert sea level to frequency
frequencies=[]
for value in values:
    norm=(value - min_val)/(max_val - min_val)
#normalized value into pitch
    freq=220+220*norm
    frequencies.append(freq)



#print info about data
print("Number of measurments:",len(values))
print("Minimum sea level:",values.min())
print("Maximum sea level:",values.max())
print("Number of frequencies:",len(frequencies))

print("\nFirst 10 frequencies:")
print(frequencies[:10])

fs = 44100

duration_per_note = 40/len(frequencies)

audio=[]

for freq in frequencies: 
    t=np.linspace(0,duration_per_note,int(fs*duration_per_note),False)

    tone=(np.sin(2*np.pi*freq*t)
    +0.3*np.sin(2*np.pi*0.5*freq*t)
    +0.2*np.sin(2*np.pi*1.5*freq*t))

    tone*=np.exp(-2*t)

    #added fade in and fade outs to reduce clicking
    fade_len=int(0.01*fs)
    if len(tone)>fade_len:
        tone[:fade_len]*=np.linspace(0,1,fade_len)
        tone[-fade_len:]*=np.linspace(1,0,fade_len)
    audio.extend(tone)

audio=np.array(audio)

max_amp = np.max(np.abs(audio))

if max_amp>0:
    audio=audio/max_amp


print("Number of years:",len(frequencies))
print("Duration per note:",duration_per_note)
print("Expected length:",len(frequencies)*duration_per_note)

print("Audio max:",np.max(np.abs(audio)))

print("Number of frequencies:",len(frequencies))
print("Duration per note:",duration_per_note)
print("Audio samples:",len(audio))
print("Expected length (seconds):",len(audio)/fs)

write("sonification.wav",fs,(audio * 32767).astype(np.int16))

print("Done")
print("File saved: sonification.wav")
