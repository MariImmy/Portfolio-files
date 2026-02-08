#working with both receiving channels on Adalm pluto simultaneously


import adi
import matplotlib.pyplot as plt
import numpy as np

# Create radio
sdr = adi.ad9361("ip:192.168.2.1")
samp_rate = 20e6

'''Configure Rx properties'''
sdr.rx_enabled_channels = [0, 1]
sdr.sample_rate = int(samp_rate)
sdr.rx_rf_bandwidth = int(samp_rate)
sdr.rx_lo = int(2.71e9)
sdr.rx_buffer_size = 8192
sdr.gain_control_mode_chan0 = "manual"
sdr.gain_control_mode_chan1 = "manual"
sdr.rx_hardwaregain_chan0 = int(40)
sdr.rx_hardwaregain_chan1 = int(40)
samples = sdr.rx() # receive samples off Pluto
while 1:
    x = sdr.rx()
    a = np.real(x[0][:])
    b = np.real(x[1][:])
    corr = np.correlate(np.real(a), np.real(b), mode='full')
    plt.clf()
    plt.plot(corr)
    # plt.ylim([-20e6, 20e6])
    plt.title("Correlation between 2 signals received from 2 different channels simultaneously")
    plt.draw()
    plt.pause(0.05)
    print(np.argmax(corr))
plt.show()#creates blocking