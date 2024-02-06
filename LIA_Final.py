import numpy as np
import math as m
from scipy.fft import fft, ifft,fftfreq
import eyes17.eyes
p=eyes17.eyes.open()
import time as t

################################ Lock in Amplifier ########################################
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
############################################################################################

#################### function to collect the signal from Expeyes ###########################
def collect_signal(stri,N_sample,N_div,f):
        t_gap = (1/(f*N_div))*10**6 #us
        t,v = p.capture1(stri,N_sample,t_gap)
        return t/1000,v
############################################################################################


f=1000
N_sample=8192
N_div=128

# p.set_sine_amp(2)
# p.set_sine(f)


V1=[]
V2=[]


for i in range(5):
    t_in,V_in=collect_signal('A1',N_sample,N_div,f)
    t_out_opamp,V_out_opamp=collect_signal('A2',N_sample,N_div,f)

    V_in_rms = np.sqrt(np.mean(np.square(V_in))) 
    V1.append(V_in_rms)
    print("The RMS of the input voltage is",V_in_rms,"V")
    V_DC = LIA(V_out_opamp,t_out_opamp,f)
    print("The output voltage is",V_DC,"V")
    V_DC=V_DC/np.sqrt(2)
    V2.append(V_DC)
    print(i+1)
    t.sleep(1)


V_out_avg=np.mean(V2)
V_in_rms_avg=np.mean(V1)
print("The RMS of the input voltage is",V_in_rms_avg,"V")
print("The output voltage is",V_out_avg,"V")


with open(f'D:\\Google_Drive\\Files\\My Drive\\Study_Stuff\\Semester-8\\Integrated_Laborotary_II\\Experiment_1_LockInAmplifier_using_Expeyes\\Codes_for_Expeyes\\Data\\MI_try_{f}Hz_fn.txt','a') as file:
    file.write(str(V_in_rms_avg)+"\t"+str(V_out_avg)+"\n")





