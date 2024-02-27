############################################################################################
import numpy as np
import math as m
from scipy.fft import fft, ifft,fftfreq
import eyes17.eyes
p=eyes17.eyes.open()
import time as tim
############################################################################################

################################ Lock in Amplifier ########################################
def LIA(V_in,t_in,f):   #V_in is the input voltage, t_in is the time list (in S),
    V_in_sin=[]         #f is the frequency
    V_in_cos=[]                      
    for i in range(len(V_in)):      
        V_in_sin.append(V_in[i]*2*np.sin(2*np.pi*f*t_in[i]))
        V_in_cos.append(V_in[i]*2*np.cos(2*np.pi*f*t_in[i]))
    V_out_sin_fft=fft(V_in_sin)
    Vx=V_out_sin_fft[0].real/len(V_out_sin_fft)
    V_out_cos_fft=fft(V_in_cos)
    Vy=V_out_cos_fft[0].real/len(V_out_cos_fft)
    return Vx,Vy
############################################################################################

#################### function to collect the signal from Expeyes ###########################
def collect_signal(stri,N_sample,N_div,f):
        t_gap = (1/(f*N_div))*10**6 #us
        t,v = p.capture1(stri,8192,2)
        # print('Time gap:',t_gap,'us')
        return t/1000,v
############################################################################################

############################# Defining input Parameters ####################################
f=1000
N_sample=8192
N_div=128
p.set_sine_amp(2)
p.set_sine(f)
p.set_pv1(1)
############################################################################################


################################## Input Voltages ##########################################
vset =[0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.1]
############################################################################################

j=0
for i in vset:
    p.set_pv1(i)
    tim.sleep(3)
    t,v=collect_signal('A1',N_sample,N_div,f)
    tim.sleep(3)
    Vx,Vy=LIA(v,t/1000,f)
    print(str(vset[j])+'\t'+str(Vx)+'\t'+str(Vy))
    with open('Data\\SS.txt','a') as file1:
        file1.write(str(vset[j])+'\t'+str(Vx)+'\t'+str(Vy)+'\n')
    j=j+1
