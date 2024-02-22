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
        t,v = p.capture1(stri,10000,2)
        print('Time gap:',t_gap,'us')
        return t/1000,v
############################################################################################

############################# Defining input Parameters ####################################
f=600
N_sample=8192
N_div=128
p.set_sine_amp(2)
p.set_sine(f)
p.set_pv1(1)
############################################################################################
vset=[0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,3.25,3.5]
vxlist_sd=[]
vylist_sd=[]

vxlist_cc=[]
vylist_cc=[]








for i in vset:
    p.set_pv1(i)
    tim.sleep(1)
    t,v=collect_signal('A2',N_sample,N_div,f)
    Vx,Vy=LIA(v,t,f)
    vxlist_sd.append(Vx)   
    vylist_sd.append(Vy)
  


with open('Data\\solar_cc.txt','w') as f:
    for i in range(len(vset)):
        f.write(str(vset[i])+'\t'+str(vxlist_sd[i])+'\t'+str(vylist_sd[i])+'\n')
    f.close()


# t1,v1=collect_signal('A2',N_sample,N_div,f)
# t,v=collect_signal('A1',N_sample,N_div,f)
# vout=LIA(v,t,f)
# print(vout)

# import matplotlib.pyplot as plt
# plt.plot(t1,v1,label='SD')
# plt.plot(t,v,label='CC')
# plt.legend()
# plt.grid()
# plt.xlim(0,0.01)
# plt.show()
