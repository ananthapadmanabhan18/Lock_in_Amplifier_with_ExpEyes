from Lock_in_Amplifier import *

f=1000 #Hz
fn=lambda x: 2*np.sin(2*np.pi*f*x)
p.load_equation(fn,[0,2*np.pi])

V_in,t_in=collect_signal('A2',8192,64,f)
V_DC = LIA(V_in,t_in,f)
print("The output voltage is",V_DC,"V")