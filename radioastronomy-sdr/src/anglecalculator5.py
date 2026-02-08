#this code repeatedly transmits and receives signals
import numpy as np
import adi
import matplotlib.pyplot as plt
import cmath
import math 

sample_rate = 1e6 # Hz
center_freq = 1000e6 # Hz
center_freq_tx=1000e6
num_samps = 100000 # number of samples per call to rx()
sdr1 = adi.ad9361("ip:192.168.2.1") #receive from both channels
sdr2 = adi.Pluto(uri="ip:192.168.2.1") #transmit and receive from only 1 channel, in this program we are using it to transmit only
sdr2.sample_rate = int(sample_rate)
sdr2.tx_enabled_channels = [0] 

sdr1.rx_enabled_channels = [0,1]  # Channel 1 for Rx
# Config Tx
sdr2.tx_rf_bandwidth = int(sample_rate) # filter cutoff, just set it to the same as sample rate
sdr2.tx_lo = int(center_freq_tx)
sdr2.tx_hardwaregain_chan0 = -20 # Increase to increase tx power, valid range is -90 to 0 dB

# Config Rx
sdr1.rx_enabled_channels = [0, 1]
sdr1.rx_lo = int(center_freq)
sdr1.rx_rf_bandwidth = int(sample_rate)
sdr1.rx_buffer_size = num_samps
sdr1.gain_control_mode_chan1 = 'manual'
sdr1.rx_hardwaregain_chan1 = 20.0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC
sdr1.gain_control_mode_chan0 = 'manual'
sdr1.rx_hardwaregain_chan0 = 0 # dB, increase to increase the receive gain, but be careful not to saturate the ADC

# 299,792,458Create transmit waveform (QPSK, 16 samples per symbol)
N = 1000000# number of samples to transmit at once
t = np.arange(N)/sample_rate
samples = (np.sin(2 * np.pi * 1000 * t) + 1)*np.exp(2.0j*np.pi*100e3*t) # Simulate a sinusoid of 100 kHz, so it should show up at 915.1 MHz at the receiver
samples *= 2**14 # The PlutoSDR expects samples to be between -2^14 and +2^14, not -1 and +1 like some SDRs

# Start the transmitter
sdr2.tx_cyclic_buffer = True # Enable cyclic buffers

fig, axs = plt.subplots(1, 2)
sdr2.tx(samples) # start transmitting
while 1:
    
    # Clear buffer just to be safe
    for i in range (0, 10):
        raw_data = sdr1.rx()

    # Receive samples
    rx_samples = sdr1.rx()
    print(rx_samples)

  

    # Frequency Domain Plot (Power Spectral Density)


    a = rx_samples[0]
    b = rx_samples[1]
    freq = np.fft.fftshift(np.fft.fftfreq(len(a), d=1/sample_rate))
    fourierTransformA= np.fft.fftshift(np.fft.fft(a))
    fourierTransformB= np.fft.fftshift(np.fft.fft(b))
    maxA=fourierTransformA[np.abs(fourierTransformA).argmax()] #channel 0
    maxB=fourierTransformB[np.abs(fourierTransformB).argmax()] #channel1
    differenceangle=cmath.phase(maxA*maxB.conjugate())
    differenceangle3=np.angle(maxA*maxB.conjugate())

    d=0.035
    timearray=[]
    arrayphi=[]
    arraypheta=[]
    c=299792458
    l=c/center_freq_tx
    #get angle of arrival
    sin_theta1=differenceangle*l/(2*math.pi*d)
    #arcsin only processes data from -1 to 1
    sin_theta=np.clip(sin_theta1, -1.0, 1.0)
    
    angle_of_arrival_deg = np.degrees(np.arcsin(sin_theta))


    angle1=math.degrees(cmath.phase(maxA))% (2 * math.pi)
    angle2=math.degrees(cmath.phase(maxB))% (2 * math.pi)
    differenceangle2=angle2-angle1

    print("Absolute value for A", np.abs(maxA))
    print("Absolute value for B", np.abs(maxB))
    print("Max value for Receiver0 %f",maxA)
    print("Max value for Receiver1 %f",maxB)
    print("Difference of angle (radians)",differenceangle)

    print("Angle of arrival (degrees)",angle_of_arrival_deg)






    axs[0].cla()
    axs[1].cla()

    axs[0].plot(freq/1e6, abs(fourierTransformA))
    axs[1].plot(freq/1e6, abs(fourierTransformB))
        # plt.ylim([-20e6, 20e6])
    axs[0].set_title(f"Channel 0 FFT Abs_max={np.abs(maxA):.3f}, Angle_difference={differenceangle:.3f} radians")
    axs[1].set_title(f"Channel 1 FFT Abs_max={np.abs(maxB):.3f} , AOA={angle_of_arrival_deg} degrees")

    axs[0].set_xlabel("Frequency (MHz)")
    axs[1].set_xlabel("Frequency (MHz)")

    axs[0].set_ylabel("Magnitude")
    axs[1].set_ylabel("Magnitude ")
    plt.pause(0.5)
    
plt.show()
  # Stop "transmitting
sdr2.tx_destroy_buffer()





#i want to know if both channels are receiving data from the transmitter 
#test if the transmitter is working 
#test if there is a difference when 2 different antennas are used(interchangably)
#positon of antenna relative to the transmitter 


#the 2 distance should be d>15cm=30 cm and d<15=10cm