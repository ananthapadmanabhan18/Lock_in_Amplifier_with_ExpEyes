import numpy as np
import math as m
from scipy.fft import fft, ifft,fftfreq
import eyes17.eyes
p=eyes17.eyes.open()


def LIA(V_in,t_in,f):
    V_in_sin=[]
    V_in_cos=[]                     #V_in is the input voltage, t_in is the time list (in S), 
    for i in range(len(V_in)):      #f is the frequency
        V_in_sin.append(V_in[i]*2*np.sin(2*np.pi*f*t_in[i]))
        V_in_cos.append(V_in[i]*2*np.cos(2*np.pi*f*t_in[i]))
    V_out_sin_fft=fft(V_in_sin)
    V_out_cos_fft=fft(V_in_cos)
    V_out= np.sqrt((V_out_sin_fft[0].real/len(V_out_sin_fft))**2+(V_out_cos_fft[0].real/len(V_out_cos_fft))**2)
    return V_out


def collect_signal(stri,N_sample,N_div,f):
    # import eyes17.eyes
    # p=eyes17.eyes.open()
    t_gap = (1/(f*N_div))*10**6 #us
    t,v = p.capture1(stri,N_sample,t_gap)
    return t/1000,v



f=1000 #Hz
N_sample = 8192
N_div=64



p.set_sine_amp(1)
p.set_sine(1000)
time,input=collect_signal('A2',N_sample,N_div,f)


print("The output voltage is",LIA(input,time,f),"V")


# import matplotlib.pyplot as plt
# plt.plot(time,input)
# plt.xlim(0,0.001)
# plt.show()
