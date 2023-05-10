import scipy
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import cont2discrete, lti, dlti, dstep

def rohrstück_continuous(volumen, volumen_stahl, länge, durchmesser):
    
    F=1 # wird nach der diskretisierung aktualisiert auf den aktuellen wert
    #volumen= 0.0015;
    #volumen_stahl = 0.00042;
    #länge= 1.230+0.12+0.11;
    #durchmesser = 0.036;


    c_oel= 1855
    p_oel= 880
    c_st = 490
    p_st = 7800
    alpha = 3370*(1 + 0.0014*60)*0.001/(durchmesser/2)**2/np.pi
    lambda__1 = alpha * länge* durchmesser * np.pi

    a__1 = lambda__1/(volumen*p_st*c_st)
    a__2 = lambda__1/(volumen_stahl*p_st*c_st)
    Tau__1 = volumen*p_oel*c_oel/(F*p_oel*c_oel)


    A=np.array([[-(1/Tau__1+a__1) , a__1],[a__2 , -a__2]])
    B=np.array([[1/Tau__1],[0]])
    C=np.array([1, 0])
    D=np.array([0])
    
    if False:
        l_system = lti(A, B, C, D)
        t, x = l_system.step(T=np.linspace(0, 5, 100))
        fig, ax = plt.subplots()
        ax.plot(t, x, label='Continuous', linewidth=3)
        
        dt = 0.1


        for method in ['zoh', 'bilinear']:#, 'euler', 'backward_diff', 'foh', 'impulse']:
            d_system = cont2discrete((A, B, C, D), dt, method=method)
            s, x_d = dstep(d_system)
            ax.step(s, np.squeeze(x_d), label=method, where='post')
        ax.axis([t[0], t[-1], x[0], 1.4])
        ax.legend(loc='best')
        fig.tight_layout()
        plt.show()
        
    return [A,B,C,D]




if __name__ == '__main__':
    from ss import rohrstück_diskret as rohr

    mydt = 0.1
    r = rohrstück_continuous(volumen= 0.0015, volumen_stahl = 0.00042, länge= 1.230+0.12+0.11, durchmesser = 0.036)
    d_system = cont2discrete(r, dt=mydt, method='bilinear')
    ss_d = rohr(d_system[0],d_system[1],d_system[2],d_system[3],100)


    print(d_system)
    
    for i in range(100):
        start_time = time.time()
        val = ss_d.update(u=[99], F=0.001)
        end_time = time.time()
        duration = end_time - start_time
        print("Iteration", i+1, "- Dauer:", duration, "Sekunden")