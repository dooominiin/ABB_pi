# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:34:38 2023

@author: domin
"""
# link zur diskretisierung : https://ch.mathworks.com/support/search.html/answers/578164-why-do-i-get-different-outputs-with-bilinear-and-c2d-sysc-ts-tustin-matlab-functions.html?fq%5B%5D=asset_type_name:answer&fq%5B%5D=category:signal/pulse-and-transition-metrics&page=1
import numpy as np
import matplotlib.pyplot as plt
import warnings
import control as ct
from scipy.signal import cont2discrete, lti, dlti, dstep

warnings.filterwarnings("error", category=RuntimeWarning)


def rohrstueck(dt):

    def f_rohr(t, x, u, params):
        p_oel = params.get('p_oel',880)
        c_oel = params.get('c_oel',1855)
        p_st = params.get('p_st',7800)
        c_st = params.get('c_st',490)
        d = params.get('d__1',0.036)
        L = params.get('L__1',1.46)
        V_st = params.get('V_st__1',0.00042)
        V = params.get('V__1',0.0015)
        dt = params.get('dt',0.1)
        
        T_oel = x[0]
        T_st = x[1]
        
        T0 = u[0]
        F = u[1]
            
        alpha =  3370*(1 + 0.0014*60)*0.001/(d/2)/(d/2)/np.pi
        lambda__1 = alpha * L * d * np.pi
        
        a1 = lambda__1/(V*p_st*c_st);
        a2 = lambda__1/(V_st*p_st*c_st);
        Tau =  V *p_oel*c_oel/(F*p_oel*c_oel);
        
        dT_oel = -(1/Tau+a1)*T_oel + a1*T_st + 1/Tau*T0
        dT_st = a2*T_oel -a2*T_st
        
        
        return x+[dT_oel,dT_st]*dt
    
    def f_rohr_output(t,x,u,params):
        return [x[0],u[1]]
    
    return ct.NonlinearIOSystem(f_rohr, f_rohr_output, inputs=('T_in','F'), outputs=('T_out','F'),states=('T_oel','T_st'),dt=dt)



def transportdelay(dt,n_Bins,volumen):   
    
    def f(t, x, u, params):
        dt = params.get('dt',0.1)
        volumen = params.get('volumen',volumen)
        number_Bins = params.get('n_Bins',1000)+1
        bins = x.copy()
        laenge_Bin = volumen/number_Bins
        output = x[len(x)-1]
    
        eingangstemperatur = u[0]
        F = u[1]
        
        if F<0:
            F=0
                
        k = number_Bins-2
        laenge_0 = F*dt
        f,m = np.divmod(laenge_0, laenge_Bin)
        f = int(f)
        m = m/laenge_Bin
        f = f
        m = m
        
        
        if f<=k:
            try:
                output = (np.sum(bins[range(k-f+1,k+1)])+bins[k-f]*(m))/(f+m)
            except RuntimeWarning:                
                output= bins[k]
        
        if f>k:
            output = (np.sum(bins)+(f-k)*eingangstemperatur)/f
            f=k+1
        
        if f<k-1:
            index_for_interpolation_T = range(k,f,-1)
            for i in index_for_interpolation_T:
                bins[i] = m * bins[i-1-f] + (1-m) * bins[i-f]
        
        if f<k:  
            bins[f] = m*eingangstemperatur + (1-m) * bins[0]
        
        if f>0:
            index_for_neue_T = range(0,f)
            for i in index_for_neue_T:
                bins[i] = eingangstemperatur
        
        dT = np.empty(np.shape(x))
        
        bins[len(x)-1] = output

        for i in range(0,len(x)):
            dT[i] = (bins[i]-x[i])/dt    

        return bins
        
      
    
    def f_out(t,x,u,params):
        #print(x)
        
        return [x[len(x)-1],u[1]]
        
    return ct.NonlinearIOSystem(f, f_out, inputs=('T_in','F'), outputs=('T_out','F'), states = n_Bins+1,dt=dt)



class Transportdelay:
    # Die Klasse Transportdelay(n_Bins, volumen, startwert) erzeug
    # ein Objekt, dass ein Transportdelay wie in einem mit Flüssigkeit 
    # durchflossenen Rohr simuliert. Das Volumen soll in m**3 angegeben werden, 
    # der Volumenstrom(F) in m**3/s. Nach der Initialisierung 
    # kann mit update(F,Eingangstemperatur,dt) ein neuer Output 
    # berechnet und ausgegeben werden. n_Bins ist die Anzahl der internen Zustände, 
    # Werte zwischen 100 und 1000 liefern genug genauigkeit.  

    def __init__(self, n_Bins, volumen, startwert):
        self.number_Bins = n_Bins
        self.bins = np.full(n_Bins, startwert, dtype=float)
        self.volumen = volumen
        self.laenge_Bin = self.volumen/self.number_Bins
        self.output = startwert 
            
    def update(self, F, eingangstemperatur, dt):
        if F < 0 :
            raise ValueError("F darf nicht kleiner 0 sein!")     
        if dt < 0 :
            raise ValueError("dt darf nicht kleiner 0 sein!")     
            
        k = self.number_Bins-1
        self.k = k
        laenge_0 = F*dt
        f,m = np.divmod(laenge_0, self.laenge_Bin)
        f = int(f)
        m = m/self.laenge_Bin
        self.f = f
        self.m = m
        
      
        if f<=k:
            try:
                self.output = (np.sum(self.bins[range(k-f+1,k+1)])+self.bins[k-f]*(m))/(f+m)
            except RuntimeWarning:                
                self.output= self.bins[k]
        
        if f>k:
            self.output = (np.sum(self.bins)+(f-k)*eingangstemperatur)/f
            f=k+1
        
        if f<k-1:
            
            index_for_interpolation_T = range(k,f,-1)
            for i in index_for_interpolation_T:
                self.bins[i] = m * self.bins[i-1-f] + (1-m) * self.bins[i-f]
        
        if f<k:   
            self.bins[f] = m*eingangstemperatur + (1-m) * self.bins[0]
        
        if f>0:
            index_for_neue_T = range(0,f)
            for i in index_for_neue_T:
                self.bins[i] = eingangstemperatur
        #print(self.output)
        return self.output
    
    
    
    
    def printme(self):
        return self.bins
        #print(self.output)
        


#x = Transportdelay(n_Bins=1000,volumen=10,startwert=100)

#t = np.linspace(0,100,101)

#for tt in t:
#    plt.plot(x.update(F = 1, eingangstemperatur = 100+10*np.cos(0.1*tt), dt = 0.5+0.5*np.sin(tt)))
#    plt.show()

#plt.show()


class rohrstück_diskrete:
    # Beschreibung
    def __init__(self,dt, startwert, volumen, volumen_stahl, länge, durchmesser):
        F=0.001 # wird nach der diskretisierung aktualisiert auf den aktuellen wert
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

        a__1 = lambda__1/(volumen*p_oel*c_oel)
        a__2 = lambda__1/(volumen_stahl*p_st*c_st)
        Tau__1 = volumen*p_oel*c_oel/(F*p_oel*c_oel)

        self.A=np.array([[-a__1-1/Tau__1 , a__1],[a__2 , -a__2]])
        self.FM = np.array([[-1/Tau__1,0],[0,0]])
        self.B=np.array([[1/Tau__1],[0]])
        self.C=np.array([1, 0])
        self.D=np.array([0])
        self.dt = dt
        self.startwert = startwert
        self.diskretisierung()

    def diskretisierung(self):
        [self.A_d,self.B_d, self.C_d, self.D_d,dt]= cont2discrete(system = (self.A, self.B, self.C, self.D), dt=self.dt, method='bilinear')
        #[self.FM_d,self.B_d, self.C_d, self.D_d,dt]= cont2discrete(system = (self.FM, self.B, self.C, self.D), dt=self.dt, method='bilinear')
        self.A_tilde = self.A_d
        #self.FM_tilde = self.FM_d
        self.B_tilde = self.B_d
        self.x = np.ones(np.ndim(self.A))*self.startwert
        self.x_neu = np.ones(np.ndim(self.A))*self.startwert
        self.u = 0
        self.y = 0

    def update(self, input, F):
        u = [input]
        # Berücksichtige aktuelles F 
        #self.FM_d[0] = self.FM_tilde[0] * F * self.dt
        #self.B_d[0] = self.B_tilde[0] * F * self.dt
        #self.A_d = self.FM_d + self.A_tilde

        # Berechne neuen Zustand
        self.x_neu = self.A_d @ self.x + self.B_d @ u
        
        # Berechne Ausgang
        self.y = self.C_d @ self.x + self.D_d @ u
        
        # Speichere den neuen Zustand
        self.x = self.x_neu
        
        return self.y

class testklasse:
    # Beschreibung
    def __init__(self,dt, startwert):
        self.C=np.array([1, 0])
        self.D=np.array([0])
        self.dt = dt
        self.startwert = startwert
        self.x = np.array([[startwert], [startwert]])
        self.F_neu = 0
        self.u_alt = np.array([0])


    def update(self, input, F_neu):
        uk1 = input
        uk = self.u_alt
        Fk = self.F_neu
        self.F_neu = F_neu
        Ts = self.dt
        xk1 = self.x[0]
        xk2 = self.x[1]

        # Berechne zustand
        self.x_neu = np.array([(6*(3325211903386097*Ts + 18014398509481984)*((4359849020494567*Ts*xk2)/36028797018963968 - xk1*((Ts*((2000*Fk)/3 + 4359849020494567/18014398509481984))/2 - 1) + (1000*Fk*Ts*uk)/3 + (1000*F_neu*Ts*uk1)/3))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904) - (13079547061483701*Ts*(xk2*((3325211903386097*Ts)/18014398509481984 - 1) - (3325211903386097*Ts*xk1)/18014398509481984))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904), (19951271420316582*Ts*((4359849020494567*Ts*xk2)/36028797018963968 - xk1*((Ts*((2000*Fk)/3 + 4359849020494567/18014398509481984))/2 - 1) + (1000*Fk*Ts*uk)/3 + (1000*F_neu*Ts*uk1)/3))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904) - ((xk2*((3325211903386097*Ts)/18014398509481984 - 1) - (3325211903386097*Ts*xk1)/18014398509481984)*(13079547061483701*Ts + 36028797018963968000*F_neu*Ts + 108086391056891904))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904)])
        #print("x: ",self.x.shape)
        #print("x_neu: ",self.x_neu.shape)
        #print("u_alt :",self.u_alt.shape,"\n")
        # Berechne Ausgang
        self.y = self.C @ self.x + self.D @ self.u_alt
        
        # Speichere den neuen Zustand
        self.x = self.x_neu
        #print("x: ",self.x.shape)

        self.u_alt = uk1

        return self.y


if __name__ == "__main__":
 
    
    rr = []  # Initialisierung der Liste rr

    for n in range(10):
        rr.append(testklasse(dt=0.1, startwert=100))  # Objekte zur Liste rr hinzufügen
    

    for i in range(100):
        input = np.array([80])
        for r in rr:
            print("input :",input)
            input = r.update(input=input,F_neu=0.001)
        print("\n")