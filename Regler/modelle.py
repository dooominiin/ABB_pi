# -*- coding: utf-8 -*-
"""
Created on Fri Feb 10 16:34:38 2023

@author: domin
"""
# link zur diskretisierung mit tustin: https://ch.mathworks.com/support/search.html/answers/578164-why-do-i-get-different-outputs-with-bilinear-and-c2d-sysc-ts-tustin-matlab-functions.html?fq%5B%5D=asset_type_name:answer&fq%5B%5D=category:signal/pulse-and-transition-metrics&page=1
import numpy as np
import time
class sensorfilter:
    # mit Tustin(Trapez-methode) diskretisiert
    def __init__(self,dt, Zeitkonstante, startwert):
        self.t_filter = 1/Zeitkonstante*np.pi
        self.dt = dt
        self.xk = 0
        self.xk1 = startwert
        self.uk1 = 0
    
    def update(self, input):
        uk = self.uk1 
        uk1 = input
        self.uk1 = uk1
        self.xk = self.xk1

        self.xk1 = ((self.dt*self.t_filter*uk)/2 - self.xk*((self.dt*self.t_filter)/2 - 1) + (self.dt*self.t_filter*uk1)/2)/((self.dt*self.t_filter)/2 + 1)
        self.output = self.xk
       
        return np.ravel(np.array([self.output]))    
    def get_t_filter(self):
        return self.t_filter

class Transportdelay:
    # Die Klasse Transportdelay(n_Bins, volumen, startwert) erzeug
    # ein Objekt, dass ein Transportdelay wie in einem mit Flüssigkeit 
    # durchflossenen Rohr simuliert. Das Volumen soll in m**3 angegeben werden, 
    # der Volumenstrom(F) in m**3/s. Nach der Initialisierung 
    # kann mit update(F,input,dt) ein neuer Output 
    # berechnet und ausgegeben werden. n_Bins ist die Anzahl der internen Zustände, 
    # Werte zwischen 100 und 1000 liefern genug genauigkeit.  

    def __init__(self, n_Bins, volumen, startwert):
        self.number_Bins = n_Bins
        self.bins = np.full(n_Bins, startwert, dtype=float)
        self.volumen = volumen
        self.laenge_Bin = self.volumen/self.number_Bins
        self.output = startwert 
            
    def update(self, F, input, dt):
     
        F = np.squeeze(F)
        input = input
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
            self.output = self.weird_division(n=(np.sum(self.bins[range(k-f+1,k+1)])+self.bins[k-f]*(m)), d=(f+m))

        if f>k:
            self.output = (np.sum(self.bins)+(f-k)*input)/f
            f=k+1
        
        if f<k-1:
            
            index_for_interpolation_T = range(k,f,-1)
            for i in index_for_interpolation_T:
                self.bins[i] = m * self.bins[i-1-f] + (1-m) * self.bins[i-f]
        
        if f<k:   
            self.bins[f] = m*input + (1-m) * self.bins[0]
        
        if f>0:
            index_for_neue_T = range(0,f)
            for i in index_for_neue_T:
                self.bins[i] = input
        return np.ravel(np.array([self.output]))
    
    
    def weird_division(self, n, d):
        return n / d if d else self.bins[self.k]    
    
    def printme(self):
        return self.bins
        
class rohrstück_1:
# Beschreibung
    def __init__(self,dt, startwert):
        self.C=np.array([1, 0])
        self.D=np.array([0])
        self.dt = dt
        self.startwert = startwert
        self.x = np.array([[startwert], [startwert]])
        self.F_neu = 0
        self.u_alt = np.array([0])

    def update(self, F, input):
        F_neu = F
        uk1 = input
        uk = self.u_alt
        Fk = self.F_neu
        self.F_neu = F_neu
        Ts = self.dt
        xk1 = self.x[0]
        xk2 = self.x[1]


        # Berechne zustand
        self.x_neu = np.array([(6*(3325211903386097*Ts + 18014398509481984)*((4359849020494567*Ts*xk2)/36028797018963968 - xk1*((Ts*((2000*Fk)/3 + 4359849020494567/18014398509481984))/2 - 1) + (1000*Fk*Ts*uk)/3 + (1000*F_neu*Ts*uk1)/3))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904) - (13079547061483701*Ts*(xk2*((3325211903386097*Ts)/18014398509481984 - 1) - (3325211903386097*Ts*xk1)/18014398509481984))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904), (19951271420316582*Ts*((4359849020494567*Ts*xk2)/36028797018963968 - xk1*((Ts*((2000*Fk)/3 + 4359849020494567/18014398509481984))/2 - 1) + (1000*Fk*Ts*uk)/3 + (1000*F_neu*Ts*uk1)/3))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904) - ((xk2*((3325211903386097*Ts)/18014398509481984 - 1) - (3325211903386097*Ts*xk1)/18014398509481984)*(13079547061483701*Ts + 36028797018963968000*F_neu*Ts + 108086391056891904))/(33030818481800283*Ts + 6650423806772194000*F_neu*Ts**2 + 36028797018963968000*F_neu*Ts + 108086391056891904)])

        # Berechne Ausgang
        self.y = self.C @ self.x + self.D @ self.u_alt
        
        # Speichere den neuen Zustand
        self.x = self.x_neu
        self.u_alt = uk1

        return self.y

class rohrstück_2:
# Beschreibung
    def __init__(self,dt, startwert):
        self.C=np.array([1, 0])
        self.D=np.array([0])
        self.dt = dt
        self.startwert = startwert
        self.x = np.array([[startwert], [startwert]])
        self.F_neu = 0
        self.u_alt = np.array([0])

    def update(self, F,input):
        F_neu = F
        uk1 = input
        uk = self.u_alt
        Fk = self.F_neu
        self.F_neu = F_neu
        Ts = self.dt
        xk1 = self.x[0]
        xk2 = self.x[1]

        # Berechne zustand
        self.x_neu = np.array([(137*(1605240352503639*Ts + 72057594037927936)*((548673005513257*Ts*xk2)/4503599627370496 - xk1*((Ts*((10000*Fk)/137 + 548673005513257/2251799813685248))/2 - 1) + (5000*Fk*Ts*uk)/137 + (5000*F_neu*Ts*uk1)/137))/(1422609156378057887*Ts + 8026201762518195000*F_neu*Ts**2 + 360287970189639680000*F_neu*Ts + 9871890383196127232) - (1202691228085059344*Ts*(xk2*((1605240352503639*Ts)/72057594037927936 - 1) - (1605240352503639*Ts*xk1)/72057594037927936))/(1422609156378057887*Ts + 8026201762518195000*F_neu*Ts**2 + 360287970189639680000*F_neu*Ts + 9871890383196127232), (219917928292998543*Ts*((548673005513257*Ts*xk2)/4503599627370496 - xk1*((Ts*((10000*Fk)/137 + 548673005513257/2251799813685248))/2 - 1) + (5000*Fk*Ts*uk)/137 + (5000*F_neu*Ts*uk1)/137))/(1422609156378057887*Ts + 8026201762518195000*F_neu*Ts**2 + 360287970189639680000*F_neu*Ts + 9871890383196127232) - (16*(xk2*((1605240352503639*Ts)/72057594037927936 - 1) - (1605240352503639*Ts*xk1)/72057594037927936)*(75168201755316209*Ts + 22517998136852480000*F_neu*Ts + 616993148949757952))/(1422609156378057887*Ts + 8026201762518195000*F_neu*Ts**2 + 360287970189639680000*F_neu*Ts + 9871890383196127232)])
        # Berechne Ausgang
        self.y = self.C @ self.x + self.D @ self.u_alt
        
        # Speichere den neuen Zustand
        self.x = self.x_neu
        self.u_alt = uk1
  
        return self.y

class mischventil:
    def __init__(self, startwert):
        self.T_M = np.array([startwert])

    def update(self, F1, F2, F3 ,T_BP2,T_WT2):
        if F1 > 0:
            self.T_M = (T_BP2*F2 + T_WT2*F3)/F1
        
        return np.ravel(np.array([self.T_M]))

class wärmetauscher:
    # Beschreibung WT
    def __init__(self,dt, startwert):
        self.C=np.array([0, 1, 0, 0])
        self.D=np.array([0, 0])
        self.dt = dt
        self.startwert = startwert
        self.x = np.array([[startwert], [startwert], [startwert], [startwert]])
        self.F_neu = 0
        self.u1_alt = np.array([0])
        self.u2_alt = np.array([0])

    def update(self, F,T_tank, T_kuehl):
        F_neu = F
        uk11 = T_tank
        uk12 = T_kuehl

        uk1 = self.u1_alt
        uk2 = self.u2_alt

        Fk = self.F_neu
        self.F_neu = F_neu
        Ts = self.dt
        xk1 = self.x[0]
        xk2 = self.x[1]
        xk3 = self.x[2]
        xk4 = self.x[3]
        
        # Berechne zustand
        self.x_neu = np.array([(3.93965e+76*xk1 + 1.33081e+76*Ts*xk1 + 2.99768e+74*Ts*xk3 + 2.99768e+74*Ts*xk4 + 2.50938e+73*Ts**2*uk2 + 8.63053e+72*Ts**3*uk2 + 6.4217e+70*Ts**4*uk2 + 2.50938e+73*Ts**2*uk12 + 8.63053e+72*Ts**3*uk12 + 6.4217e+70*Ts**4*uk12 + 1.12159e+75*Ts**2*xk1 + 4.43264e+71*Ts**2*xk2 - 7.6713e+71*Ts**3*xk1 + 1.031e+74*Ts**2*xk3 + 1.11973e+71*Ts**3*xk2 - 6.4217e+70*Ts**4*xk1 + 5.29119e+73*Ts**2*xk4 + 7.6713e+71*Ts**3*xk3 + 3.85252e+71*Ts**3*xk4 + 1.10428e+79*F_neu**2*Ts**2*uk11 + 3.73026e+78*F_neu**2*Ts**3*uk11 + 3.1502e+77*F_neu**2*Ts**4*uk11 + 6.59581e+77*Fk*Ts*uk1 + 6.59581e+77*F_neu*Ts*uk11 - 6.59581e+77*Fk*Ts*xk1 + 6.59581e+77*F_neu*Ts*xk1 + 2.27825e+77*Fk*Ts**2*uk1 + 2.05076e+76*Fk*Ts**3*uk1 + 1.42234e+74*Fk*Ts**4*uk1 + 4.20124e+74*F_neu*Ts**3*uk2 + 1.41297e+74*F_neu*Ts**4*uk2 + 2.27825e+77*F_neu*Ts**2*uk11 + 2.05076e+76*F_neu*Ts**3*uk11 + 4.20124e+74*F_neu*Ts**3*uk12 + 1.42234e+74*F_neu*Ts**4*uk11 + 1.41297e+74*F_neu*Ts**4*uk12 - 2.27825e+77*Fk*Ts**2*xk1 - 2.05039e+76*Fk*Ts**3*xk1 + 2.17788e+77*F_neu*Ts**2*xk1 - 3.71059e+72*Fk*Ts**3*xk2 - 1.41297e+74*Fk*Ts**4*xk1 + 1.71244e+76*F_neu*Ts**3*xk1 - 9.37335e+71*Fk*Ts**4*xk2 + 5.01876e+75*F_neu*Ts**2*xk3 + 3.71059e+72*F_neu*Ts**3*xk2 - 1.42234e+74*F_neu*Ts**4*xk1 + 5.01876e+75*F_neu*Ts**2*xk4 + 1.68792e+75*F_neu*Ts**3*xk3 + 9.37335e+71*F_neu*Ts**4*xk2 + 8.4767e+74*F_neu*Ts**3*xk4 + 1.10428e+79*Fk*F_neu*Ts**2*uk1 + 3.73026e+78*Fk*F_neu*Ts**3*uk1 + 3.1502e+77*Fk*F_neu*Ts**4*uk1 - 1.10428e+79*Fk*F_neu*Ts**2*xk1 - 3.73026e+78*Fk*F_neu*Ts**3*xk1 - 3.1502e+77*Fk*F_neu*Ts**4*xk1)/(1.39077e+76*Ts + 4.55651e+77*F_neu*Ts**2 + 4.10116e+76*F_neu*Ts**3 + 2.83531e+74*F_neu*Ts**4 + 1.32823e+75*Ts**2 + 1.77583e+73*Ts**3 + 6.4217e+70*Ts**4 + 1.10428e+79*F_neu**2*Ts**2 + 3.73026e+78*F_neu**2*Ts**3 + 3.1502e+77*F_neu**2*Ts**4 + 1.31916e+78*F_neu*Ts + 3.93965e+76), (3.93965e+76*xk2 + 1.33081e+76*Ts*xk2 + 2.99768e+74*Ts*xk3 + 2.99768e+74*Ts*xk4 + 2.50938e+73*Ts**2*uk2 + 8.63053e+72*Ts**3*uk2 + 6.4217e+70*Ts**4*uk2 + 2.50938e+73*Ts**2*uk12 + 8.63053e+72*Ts**3*uk12 + 6.4217e+70*Ts**4*uk12 + 4.43264e+71*Ts**2*xk1 + 1.12159e+75*Ts**2*xk2 + 1.11973e+71*Ts**3*xk1 + 1.031e+74*Ts**2*xk3 - 7.6713e+71*Ts**3*xk2 + 5.29119e+73*Ts**2*xk4 + 7.6713e+71*Ts**3*xk3 - 6.4217e+70*Ts**4*xk2 + 3.85252e+71*Ts**3*xk4 + 1.10428e+79*F_neu**2*Ts**2*uk11 + 3.73026e+78*F_neu**2*Ts**3*uk11 + 3.1502e+77*F_neu**2*Ts**4*uk11 + 6.59581e+77*Fk*Ts*xk1 - 6.59581e+77*Fk*Ts*xk2 + 6.59581e+77*F_neu*Ts*xk1 + 6.59581e+77*F_neu*Ts*xk2 + 3.71059e+72*Fk*Ts**3*uk1 + 9.37335e+71*Fk*Ts**4*uk1 + 8.40248e+74*F_neu*Ts**3*uk2 + 2.82594e+74*F_neu*Ts**4*uk2 + 3.71059e+72*F_neu*Ts**3*uk11 + 8.40248e+74*F_neu*Ts**3*uk12 + 9.37335e+71*F_neu*Ts**4*uk11 + 2.82594e+74*F_neu*Ts**4*uk12 + 2.27825e+77*Fk*Ts**2*xk1 - 2.27825e+77*Fk*Ts**2*xk2 + 2.05039e+76*Fk*Ts**3*xk1 + 2.17788e+77*F_neu*Ts**2*xk1 - 2.05076e+76*Fk*Ts**3*xk2 + 1.41297e+74*Fk*Ts**4*xk1 + 2.17788e+77*F_neu*Ts**2*xk2 + 1.71281e+76*F_neu*Ts**3*xk1 - 1.42234e+74*Fk*Ts**4*xk2 + 1.00375e+76*F_neu*Ts**2*xk3 + 1.71281e+76*F_neu*Ts**3*xk2 - 1.41297e+74*F_neu*Ts**4*xk1 + 1.00375e+76*F_neu*Ts**2*xk4 + 3.37584e+75*F_neu*Ts**3*xk3 - 1.41297e+74*F_neu*Ts**4*xk2 + 1.69534e+75*F_neu*Ts**3*xk4 + 1.10428e+79*Fk*F_neu*Ts**2*uk1 + 3.73026e+78*Fk*F_neu*Ts**3*uk1 + 3.1502e+77*Fk*F_neu*Ts**4*uk1 - 1.10428e+79*Fk*F_neu*Ts**2*xk2 - 3.73026e+78*Fk*F_neu*Ts**3*xk2 - 3.1502e+77*Fk*F_neu*Ts**4*xk2)/(1.39077e+76*Ts + 4.55651e+77*F_neu*Ts**2 + 4.10116e+76*F_neu*Ts**3 + 2.83531e+74*F_neu*Ts**4 + 1.32823e+75*Ts**2 + 1.77583e+73*Ts**3 + 6.4217e+70*Ts**4 + 1.10428e+79*F_neu**2*Ts**2 + 3.73026e+78*F_neu**2*Ts**3 + 3.1502e+77*F_neu**2*Ts**4 + 1.31916e+78*F_neu*Ts + 3.93965e+76), (0.125*(3.15172e+77*xk3 + 5.27665e+76*Ts*uk2 + 5.27665e+76*Ts*uk12 + 4.6604e+74*Ts*xk1 + 4.6604e+74*Ts*xk2 + 4.7963e+75*Ts*xk3 + 9.71526e+75*Ts**2*uk2 + 1.38385e+74*Ts**3*uk2 + 5.13736e+71*Ts**4*uk2 + 9.71526e+75*Ts**2*uk12 + 1.38385e+74*Ts**3*uk12 + 5.13736e+71*Ts**4*uk12 + 8.22603e+73*Ts**2*xk1 + 8.22603e+73*Ts**2*xk2 + 5.98938e+71*Ts**3*xk1 - 8.97273e+75*Ts**2*xk3 + 5.98938e+71*Ts**3*xk2 + 3.54611e+72*Ts**2*xk4 - 1.35929e+74*Ts**3*xk3 + 2.69824e+70*Ts**3*xk4 - 5.13736e+71*Ts**4*xk3 + 1.47904e+79*F_neu**2*Ts**3*uk2 + 2.4981e+78*F_neu**2*Ts**4*uk2 + 1.30631e+77*F_neu**2*Ts**3*uk11 + 1.47904e+79*F_neu**2*Ts**3*uk12 + 2.20635e+76*F_neu**2*Ts**4*uk11 + 2.4981e+78*F_neu**2*Ts**4*uk12 + 6.53153e+76*F_neu**2*Ts**3*xk1 + 8.83424e+79*F_neu**2*Ts**2*xk3 + 6.53153e+76*F_neu**2*Ts**3*xk2 + 1.10318e+76*F_neu**2*Ts**4*xk1 + 1.10318e+76*F_neu**2*Ts**4*xk2 - 2.52016e+78*F_neu**2*Ts**4*xk3 + 1.05533e+79*F_neu*Ts*xk3 + 3.90125e+75*Fk*Ts**2*uk1 + 6.88607e+74*Fk*Ts**3*uk1 + 5.01375e+72*Fk*Ts**4*uk1 + 1.76685e+78*F_neu*Ts**2*uk2 + 3.11865e+77*F_neu*Ts**3*uk2 + 2.26323e+75*F_neu*Ts**4*uk2 + 3.90125e+75*F_neu*Ts**2*uk11 + 1.76685e+78*F_neu*Ts**2*uk12 + 6.88607e+74*F_neu*Ts**3*uk11 + 3.11865e+77*F_neu*Ts**3*uk12 + 5.01375e+72*F_neu*Ts**4*uk11 + 2.26323e+75*F_neu*Ts**4*uk12 - 3.90125e+75*Fk*Ts**2*xk2 + 1.5605e+76*F_neu*Ts**2*xk1 - 6.88607e+74*Fk*Ts**3*xk2 + 1.17038e+76*F_neu*Ts**2*xk2 + 2.63569e+75*F_neu*Ts**3*xk1 - 5.01375e+72*Fk*Ts**4*xk2 + 8.03002e+76*F_neu*Ts**2*xk3 + 2.00645e+75*F_neu*Ts**3*xk2 - 3.01056e+77*F_neu*Ts**3*xk3 + 5.01375e+72*F_neu*Ts**4*xk2 + 8.90541e+73*F_neu*Ts**3*xk4 - 2.26825e+75*F_neu*Ts**4*xk3 + 1.30631e+77*Fk*F_neu*Ts**3*uk1 + 2.20635e+76*Fk*F_neu*Ts**4*uk1 - 6.53153e+76*Fk*F_neu*Ts**3*xk1 - 6.53153e+76*Fk*F_neu*Ts**3*xk2 - 1.10318e+76*Fk*F_neu*Ts**4*xk1 - 1.10318e+76*Fk*F_neu*Ts**4*xk2))/(1.39077e+76*Ts + 4.55651e+77*F_neu*Ts**2 + 4.10116e+76*F_neu*Ts**3 + 2.83531e+74*F_neu*Ts**4 + 1.32823e+75*Ts**2 + 1.77583e+73*Ts**3 + 6.4217e+70*Ts**4 + 1.10428e+79*F_neu**2*Ts**2 + 3.73026e+78*F_neu**2*Ts**3 + 3.1502e+77*F_neu**2*Ts**4 + 1.31916e+78*F_neu*Ts + 3.93965e+76), (0.125*(3.15172e+77*xk4 + 4.6604e+74*Ts*xk1 + 4.6604e+74*Ts*xk2 + 1.05533e+77*Ts*xk3 + 4.7963e+75*Ts*xk4 + 8.83424e+75*Ts**2*uk2 + 1.34737e+74*Ts**3*uk2 + 5.13736e+71*Ts**4*uk2 + 8.83424e+75*Ts**2*uk12 + 1.34737e+74*Ts**3*uk12 + 5.13736e+71*Ts**4*uk12 + 1.60285e+74*Ts**2*xk1 + 1.60285e+74*Ts**2*xk2 + 1.19263e+72*Ts**3*xk1 + 1.60955e+75*Ts**2*xk3 + 1.19263e+72*Ts**3*xk2 - 8.97273e+75*Ts**2*xk4 + 6.13704e+72*Ts**3*xk3 - 1.35929e+74*Ts**3*xk4 - 5.13736e+71*Ts**4*xk4 + 2.47623e+78*F_neu**2*Ts**4*uk2 + 1.30631e+77*F_neu**2*Ts**3*uk11 + 4.39339e+76*F_neu**2*Ts**4*uk11 + 2.47623e+78*F_neu**2*Ts**4*uk12 + 6.53153e+76*F_neu**2*Ts**3*xk1 + 6.53153e+76*F_neu**2*Ts**3*xk2 + 2.19669e+76*F_neu**2*Ts**4*xk1 + 8.83424e+79*F_neu**2*Ts**2*xk4 + 2.95808e+79*F_neu**2*Ts**3*xk3 + 2.19669e+76*F_neu**2*Ts**4*xk2 - 2.52016e+78*F_neu**2*Ts**4*xk4 + 1.05533e+79*F_neu*Ts*xk4 + 3.90125e+75*Fk*Ts**2*uk1 + 1.34176e+75*Fk*Ts**3*uk1 + 9.98361e+72*Fk*Ts**4*uk1 + 2.95808e+77*F_neu*Ts**3*uk2 + 2.25826e+75*F_neu*Ts**4*uk2 + 3.90125e+75*F_neu*Ts**2*uk11 + 1.34176e+75*F_neu*Ts**3*uk11 + 2.95808e+77*F_neu*Ts**3*uk12 + 9.98361e+72*F_neu*Ts**4*uk11 + 2.25826e+75*F_neu*Ts**4*uk12 - 3.90125e+75*Fk*Ts**2*xk2 + 1.5605e+76*F_neu*Ts**2*xk1 - 1.34176e+75*Fk*Ts**3*xk2 + 1.17038e+76*F_neu*Ts**2*xk2 + 5.2483e+75*F_neu*Ts**3*xk1 - 9.98361e+72*Fk*Ts**4*xk2 + 3.53369e+78*F_neu*Ts**2*xk3 + 3.96591e+75*F_neu*Ts**3*xk2 + 8.03002e+76*F_neu*Ts**2*xk4 + 2.6977e+76*F_neu*Ts**3*xk3 + 9.98361e+72*F_neu*Ts**4*xk2 - 3.01056e+77*F_neu*Ts**3*xk4 - 2.26825e+75*F_neu*Ts**4*xk4 + 1.30631e+77*Fk*F_neu*Ts**3*uk1 + 4.39339e+76*Fk*F_neu*Ts**4*uk1 - 6.53153e+76*Fk*F_neu*Ts**3*xk1 - 6.53153e+76*Fk*F_neu*Ts**3*xk2 - 2.19669e+76*Fk*F_neu*Ts**4*xk1 - 2.19669e+76*Fk*F_neu*Ts**4*xk2))/(1.39077e+76*Ts + 4.55651e+77*F_neu*Ts**2 + 4.10116e+76*F_neu*Ts**3 + 2.83531e+74*F_neu*Ts**4 + 1.32823e+75*Ts**2 + 1.77583e+73*Ts**3 + 6.4217e+70*Ts**4 + 1.10428e+79*F_neu**2*Ts**2 + 3.73026e+78*F_neu**2*Ts**3 + 3.1502e+77*F_neu**2*Ts**4 + 1.31916e+78*F_neu*Ts + 3.93965e+76)])

        # Berechne Ausgang
        self.y = self.C @ self.x + self.D @ np.array([self.u1_alt,self.u2_alt])
        
        # Speichere den neuen Zustand
        self.x = self.x_neu
        self.u1_alt = uk11
        self.u2_alt = uk12

        return self.y

class F_nach_r:
    # Beschreibung F nach r
    def update(F,r):
        if r>0.999:
            r=0.999
        else: 
            if r<0.001:
                r=0.001
        F1 = F
        F3 = F1 * r
        F2 = F1 - F3
        return [F1, F2 ,F3]

class PIDRegler:
    # Achtung forward euler, nicht immer stabil
    def __init__(self, Kp, Ki, Kd, dt, minimalwert, maximalwert):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.dt = dt
        self.minimalwert = minimalwert
        self.maximalwert = maximalwert
        self.letzter_fehler = 0
        self.integral = 0

    def set_limits(self, minimalwert, maximalwert):
        self.minimalwert = minimalwert
        self.maximalwert = maximalwert
    
    def update(self, fehler):
        fehler = fehler
        # Proportionaler Term
        P = self.Kp * fehler

        # Integraler Term
        self.integral = self.integral + self.Ki * fehler * self.dt
        self.integral = max(self.minimalwert, min(self.maximalwert , self.integral))
        I = self.integral
        #print("I: ",I, "fehler: ",fehler)
        # Differentialer Term
        differential = (fehler - self.letzter_fehler) / self.dt
        D = self.Kd * differential

        # Steuerwert berechnen
        stellwert = P + I + D

        # Letzten Fehler aktualisieren
        self.letzter_fehler = fehler

        if stellwert > self.maximalwert:
            stellwert = self.maximalwert
        elif stellwert < self.minimalwert:
            stellwert = self.minimalwert
            
        return stellwert

class PI_Regler:
 # mit Tustin(Trapez-methode) diskretisiert
    def __init__(self, Kp, Ki, dt, minimalwert, maximalwert, antiwindup_upper, antiwindup_lower, name):
        self.Kp = Kp
        self.Ki = Ki
        self.dt = dt
        self.minimalwert = minimalwert
        self.maximalwert = maximalwert
        self.antiwindup_upper = antiwindup_upper
        self.antiwindup_lower = antiwindup_lower
        self.name  = name
        self.xk = 0
        self.xk1 = 0
        self.uk1 = 0

    def set_limits(self, minimalwert, maximalwert, antiwindup_upper, antiwindup_lower):
        self.minimalwert = minimalwert
        self.maximalwert = maximalwert
        self.antiwindup_upper = antiwindup_upper
        self.antiwindup_lower = antiwindup_lower

    def update(self, fehler):
        uk = self.uk1 
        uk1 = fehler
        self.uk1 = uk1
        self.xk = self.xk1
        ## hier anti wind up einfügen
        #print(self.name,"\t\tx: ",self.xk)
        if self.xk >= self.antiwindup_upper:
            self.xk = self.antiwindup_upper
            #print(self.name," maximalwert erreicht!")
        elif self.xk < self.antiwindup_lower:
            self.xk = self.antiwindup_lower
            #print(self.name," minimalwert erreicht!")



        self.xk1 = self.xk + (self.dt*self.Ki*uk)/2 + (self.dt*self.Ki*uk1)/2
        stellwert = self.xk + self.Kp * uk1

        if stellwert > self.maximalwert:
            stellwert = self.maximalwert
        elif stellwert < self.minimalwert:
            stellwert = self.minimalwert
            
        return stellwert    

    def adaptParameters(self,F, t_filter,T_tank,T_kuehl):
        # soll für die dynamische anpassung an das Wärmetauschermodell genutzt werden und past die parameter des reglers an den maximal möglichen gain des systems an. Der Wärmetauscher hat maximal etwa 100kW kühlleistung.
        P_max = 100000
        coel = 2000
        poel = 1000     
        max_gain = -P_max/(F*coel*poel)
        max_gain = T_kuehl-T_tank

        self.Kp = 1/max_gain/self.dt/t_filter*2*np.pi/20
        self.Ki = t_filter * self.Kp
        #print(self.name, "   ki: ",self.Ki,"   Kp: ", self.Kp, "     max gain: ",max_gain)

    def adaptParameters_K(self,F):
        # soll für die dynamische anpassung an das Wärmetauschermodell genutzt werden und past die parameter des reglers an den maximal möglichen gain des systems an. Der Wärmetauscher hat maximal etwa 100kW kühlleistung.

        self.Kp = 0.6 
        self.Ki = self.Kp * 0.06 / 0.001 *F
        #print(self.name, "   ki: ",self.Ki,"   Kp: ", self.Kp)

import numpy as np

class LookupTable:
    def __init__(self):
        self.keys = np.linspace(0, 1, 11)
        self.values = np.array([0	,0.400799732573815	,0.619636162348070	,0.744447185364894,	0.811554345050153,	0.859176897591362,	0.900500448644506	,0.938703450255423,	0.974730918438370,	1.00620288454483,	1.03073937992630])
    
    def map_value(self, value):
        mapped_value = np.interp(value, self.keys, self.values)
        return mapped_value

class testklasse:
    # Beschreibung F nach r
    def update(F,r):
        if r>0.999:
            r=0.999
        else: 
            if r<0.001:
                r=0.001
        F1 = F
        F3 = F1 * r
        F2 = F1 - F3
        return [F1, F2 ,F3]


if __name__ == "__main__":
    
    
    l = LookupTable()
    print(l.map_value(14))

