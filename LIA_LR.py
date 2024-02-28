############################################################################################
import numpy as np
import math as m
from scipy.fft import fft, ifft,fftfreq
import eyes17.eyes
p=eyes17.eyes.open()
import time as tim
###########################################################################################


############################################ Lock in Amplifier ####################################################
def LIA(V_in,t_in,f):   #V_in is the input voltage, t_in is the time list (in S),
    V_in_sin=[]         #f is the frequency
    V_in_cos=[]                      
    for i in range(len(V_in)):      
        V_in_sin.append(V_in[i]*2*np.sin(2*np.pi*f*t_in[i]))
        V_in_cos.append(V_in[i]*2*np.cos(2*np.pi*f*t_in[i]))
    V_out_sin_fft=fft(V_in_sin)
    V_out_cos_fft=fft(V_in_cos)
    V_out= np.sqrt((V_out_sin_fft[0].real/len(V_out_sin_fft))**2+(V_out_cos_fft[0].real/len(V_out_cos_fft))**2)
    return V_out
###################################################################################################################


############################# Defining input Parameters ####################################
f=1000
p.set_sine(f)
p.set_sine_amp(2)
p.set_pv1(2)
############################################################################################



t1,v1 = p.capture1('A2',8192,2)
t1=[t1[i]/1000 for i in range(len(t1))]
V_in_rms=LIA(v1,t1,f)/np.sqrt(2)

tim.sleep(3)

t2,v2 = p.capture1('A1',8192,2)
t2=[t2[i]/1000 for i in range(len(t2))]
V_out_rms = LIA(v2,t2,f)/np.sqrt(2)

print(V_in_rms,V_out_rms)
with open(f'Data\\Low_Resistance\\LR_{f}.txt','a') as file1:
    file1.write(str(V_in_rms)+'\t'+str(V_out_rms)+'\n')