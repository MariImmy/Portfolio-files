#simulate a transmitter of signal and 2 signal receivers 
#The main transmitted signal 
import numpy as np
import adi
import matplotlib.pyplot as plt 
import cmath
import math
c=299792458
#you will be creating coordinates to create a simulation of your signals 
R1_x=0
R1_y=0
R2_x=0
R2_y=0
T1_x=0
T1_y=0
def coordinate(r1_x,r1_y,r2_x,r2_y,t1_x,t1_y):
    #instead of saying 'return'; set the variables to global 
    global R1_x, R1_y, R2_x, R2_y, T1_x, T1_y
    R1_x=r1_x
    R1_y=r1_y
    R2_x=r2_x
    R2_y=r2_y
    T1_x=t1_x
    T1_y=t1_y


coordinate(0,0,1,0,0,1)

#distance between transmitter and receiver

#from R1 to T1
d1=np.sqrt((T1_x-R1_x)**2+(T1_y-R1_y)**2) #use ** instead of ^, as ^ is used for BITWISE Operation
#from R2 to T1
d2=np.sqrt((T1_x-R2_x)**2+(T1_y-R2_y)**2)
d_difference=d2-d1
#time for transmitter signal to get to receiver
tao1=d1/c
tao2=d2/c
print('Time and location for R1: ',d1,tao1 )
print('Time and location for R2: ',d2,tao2 )

#time difference between the receivers
tao_difference=tao2-tao1
print('Time and location difference: ',np.abs(d_difference),np.abs(tao_difference) )

#angles between transmitter and receiver


sample_rate = 1e6
N = 1000000# number of samples to transmit at once
t = np.arange(N)/sample_rate
r1_signal_samples=np.exp((2.0j*np.pi*100e3*t)-tao1)

r2_signal_samples=np.exp((2.0j*np.pi*100e3*t)-tao2)

t1_signal_samples=np.exp((2.0j*np.pi*100e3*t)-0)


#argument of difference in tao


center_freq = 1000e6 # Hz
def angles(r_x,r_y):
    difference_x=T1_x-r_x
    difference_y=T1_y-r_y

    angle= np.arctan2(difference_y,difference_x)
    return angle

angleR1=angles(R1_x, R1_y)
angleR2=angles(R2_x, R2_y)
angles_difference=angleR2-angleR1
print('Angle for R1: ',angleR1 )
print('Angle for R2: ',angleR2 )
print('Angle Difference: ',angles_difference )





d=0.15
timearray=[]
arrayphi=[]
arraypheta=np.linspace(-90, 90, num=1000)
c=299792458
l=c/center_freq
#plotting the time vs angle and the phi vs angle graph
for i in range(len(arraypheta)):
    phi=np.sin(np.radians(arraypheta[i]))*2*(1/l)*math.pi*d   # rad
    t=d*np.sin(np.radians(arraypheta[i]))/c  # sec
    arrayphi.append(phi)
  
    timearray.append(t)
print(l)
print(d)
#phi difference vs pheta
plt.figure(figsize=(10, 5))
plt.plot(arraypheta, arrayphi)
plt.xlabel("Angle(degrees)")
plt.ylabel("Phi difference(radians)")
plt.title("Phi difference vs angle")

wrappedphi=[]
for i in range(len(arraypheta)):
   # rad
    t=d*np.sin(np.radians(arraypheta[i]))/c  # sec
    phi1 = 2*math.pi*center_freq*t
    phi=np.angle(np.exp(1j*phi1))
    wrappedphi.append(phi)
  


#wrapped phi difference vs pheta
plt.figure(figsize=(10, 5))
plt.plot(arraypheta, wrappedphi)
plt.xlabel("Angle(degrees)")
plt.ylabel("Wrapped Phi difference(radians)")
plt.title("Wrapped Phi difference vs angle")

#time difference vs pheta
plt.figure(figsize=(10, 5))
plt.plot(arraypheta, timearray)
plt.xlabel("Angle")
plt.ylabel("Time difference")
plt.title("TIme difference vs angle")
   
array_measuredphase=np.linspace(-math.pi,math.pi,num=1000) 
array_calculated_AOA_deg=np.arcsin(array_measuredphase/(2*math.pi*center_freq)*c/d)/math.pi*180



#calculated angle of arrival vs measured phase in range -pi to +pi 
plt.figure(figsize=(10, 5))
plt.plot(array_measuredphase, array_calculated_AOA_deg)
plt.xlabel("Measured phase(radians)")
plt.ylabel("Calculated angle of arrival(radians)")
plt.title("Calculated angle of arrival vs measured phase")
plt.show()