#bandwidth spectrum analyzer

import numpy as np
import adi
import matplotlib.pyplot as plt
from time import sleep


low=0
high=0
def frequencyinit(a,b):
    if a<b:
        low=a
        high=b
    else:
        high=a
        low=b

    return low, high

        


num_samps = 10000 # number of samples returned per call to rx()
sdr = adi.ad9361("ip:192.168.2.1")
#sdr = adi.Pluto('ip:192.168.2.1')
sdr.gain_control_mode_chan0 = 'manual'
sdr.rx_hardwaregain_chan0 = 70.0 # dB
sample_rate=2e6
sdr.sample_rate = int(sample_rate)
#bandwidth
bw=2e6#this creates more defined bands, the smaller the value, the narrower the filter. usually the sample_rate is the same as bandwidth 
sdr.rx_buffer_size = num_samps
df = sample_rate/num_samps
#to change between channels
sdr.rx_enabled_channels=[0]
sdr.rx_rf_bandwidth = int(bw)
low=86e6
high=11e7
samples = sdr.rx() # receive samples off Pluto
fourierarray=[]
frequencyinit(86e6, 110e6)
print(low)

center_freqs = np.arange(
    low+ bw/2,
    high-bw/2,
    sample_rate
)

#each chunk is to produce a frequency axis and power value
fourierarray=[]
freq=[]



df = sample_rate / num_samps
samplingInterval = 1 / sample_rate 
print("hi")
print(center_freqs)
  # interactive mode ON to stop blocking(plt.show does blocking)



plt.figure(figsize=(10, 5))
#plt.ion()   
for i in center_freqs:
            
    sdr.rx_lo = int(i)
    iq=sdr.rx()

                #capture iq data
        
                
                
                #apply fft window to iq data to reduce fft artifacts
            
                #fft(iq) for fourier transform and fftshift() to shift the transformed signal to centre
    fourierTransformA= np.fft.fftshift(np.fft.fft(iq))
                
                #convert the fourier transform to power
            
                #frequencies 
    frequenciesa = np.fft.fftshift(np.fft.fftfreq(num_samps, samplingInterval))+i
    freq.extend(frequenciesa/(1e6))
            

    fourierarray.extend(abs(fourierTransformA))
    

    #plt.clf()  #we don't need clf command if weplt.pause(1) plt multiple figures

            #plt.figure(figsize=(10,5))
    
    plt.plot(frequenciesa/(1e6), abs(fourierTransformA))
    plt.xlabel("Frequency (MHz)")
    plt.ylabel("Magnitude (linear)")
    plt.title("Wide Band Spectrum (Raw FFT)")
    plt.grid(True)
    plt.draw()
    plt.pause(0.5)
             
    
#plt.ioff()#switch off interactive mode


plt.figure(figsize=(10, 5))
plt.plot(freq, fourierarray)
plt.xlabel("Frequency (MHz)")
plt.ylabel("Magnitude (linear)")
plt.title("Wide-band Spectrum (Raw FFT)")
plt.grid(True)
plt.show()

#plt.close('all')


    

#magnitude spectrum for data capture must either be 20 log10(|FFT|)  vs  frequency
#or it must be |FFT| vs frequency s

    


print(fourierarray[0:10])




#Plot the frequency domain representation:
#plt.figure(figsize=(10, 6))
#plt.plot( frequencies, np.abs(fourierTransform))
#plt.xlabel('Frequency (Hz)')
#plt.ylabel('Amplitude')
#plt.title('Fourier Transform depicting the frequency components')
#plt.grid(True)
#plt.show()   


#PLot time domain data 
#plt.figure(figsize=(10, 6))
#plt.plot(  np.real(samples))
#plt.xlabel('Time (s)')
#plt.ylabel('Amplitude')
#plt.title('Time domain data')
#plt.grid(True)
#plt.show() 

    




