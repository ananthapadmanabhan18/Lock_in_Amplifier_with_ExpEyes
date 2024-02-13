import numpy as np
import math as m
from scipy.fft import fft, ifft,fftfreq
import eyes17.eyes
p=eyes17.eyes.open()
import time as tim

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
    # V_out= np.sqrt((V_out_sin_fft[0].real/len(V_out_sin_fft))**2+(V_out_cos_fft[0].real/len(V_out_cos_fft))**2)
    return Vx,Vy
############################################################################################

#################### function to collect the signal from Expeyes ###########################
def collect_signal(stri,N_sample,N_div,f):
        t_gap = (1/(f*N_div))*10**6 #us
        t,v = p.capture1(stri,N_sample,t_gap)
        return t/1000,v
############################################################################################

############################# Defining input Parameters ####################################
f=1000
N_sample=8192
N_div=128
p.set_sine_amp(2)
p.set_sine(f)
p.set_pv1(0.2)
############################################################################################
vset=[0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5]
vxlist=[]
vylist=[]

for i in vset:
    p.set_pv1(i)
    tim.sleep(0.5)
    t,v=collect_signal('A2',N_sample,N_div,f)
    Vx,Vy=LIA(v,t,f)
    vxlist.append(Vx)   
    vylist.append(Vy)


with open('Data\\1000hz_sd.txt','w') as f:
    for i in range(len(vset)):
        f.write(str(vset[i])+'\t'+str(vxlist[i])+'\t'+str(vylist[i])+'\n')
    f.close()


# t,v=collect_signal('A2',N_sample,N_div,f)
# vout=LIA(v,t,f)
# print(vout)

# import matplotlib.pyplot as plt
# plt.plot(t,v)
# plt.xlim(0,0.01)
# plt.show()
