from Regler.modelle import Transportdelay
from Regler.modelle import rohrstück_1
from Regler.modelle import rohrstück_2
from Regler.modelle import wärmetauscher
from Regler.modelle import F_nach_r
from Regler.modelle import mischventil
from Regler.modelle import PI_Regler
from Regler.modelle import sensorfilter

import numpy as np
import matplotlib.pyplot as plt

# Implementiert einen Smithpredicter, der die eigentliche regelung vornimmt. 


class Smithpredictor:
    def __init__(self, dt):
        self.dt = dt
        startwert = 70
        self.zähler = 0

        self.r = 0.5
        self.T_V_tilde = startwert
        self.F1 = 0.001
        self.F2 = 0.0005
        self.F3 = 0.0005


        self.wt = wärmetauscher(dt=self.dt, startwert=startwert)
    
        self.tot1 = Transportdelay(n_Bins=1000, volumen=0.001486098988854, startwert=startwert)
        self.tot2 = Transportdelay(n_Bins=1000, volumen=0.005972953032638, startwert=startwert)
        self.tot3 = Transportdelay(n_Bins=1000, volumen=0.003664353671147, startwert=startwert)
        self.tot4 = Transportdelay(n_Bins=1000, volumen=0.020497478347979, startwert=startwert)

        self.rohr1 = rohrstück_1(dt=self.dt, startwert=startwert)
        self.rohr2 = rohrstück_2(dt=self.dt, startwert=startwert)

        self.misch = mischventil(startwert=startwert)    









        self.filter_V_tilde = sensorfilter(dt = dt, Zeitkonstante=10,startwert = startwert)
        self.filter_V = sensorfilter(dt = dt, Zeitkonstante=10,startwert = startwert)
        self.filter_T_tilde = sensorfilter(dt = dt, Zeitkonstante=10,startwert = startwert)
        self.filter_T = sensorfilter(dt = dt, Zeitkonstante=10,startwert = startwert)



        self.F_regler = PI_Regler(Kp = -1, Ki = 0 , dt = self.dt, minimalwert=-60, maximalwert=60,antiwindup_lower=-99,antiwindup_upper=99, name = "F")
        self.F_regler = PI_Regler(Kp = 0, Ki = 0 , dt = self.dt, minimalwert=-60, maximalwert=60,antiwindup_lower=-99,antiwindup_upper=99, name = "F")
        
        self.K_regler = PI_Regler(Kp = 0.6, Ki = 0.06/0.6, dt = self.dt, minimalwert=-200, maximalwert=200,antiwindup_lower=-99,antiwindup_upper=99, name = "K")
        self.K_regler = PI_Regler(Kp = 0, Ki = 0, dt = self.dt, minimalwert=-200, maximalwert=200,antiwindup_lower=-99,antiwindup_upper=99, name = "K")
        
        self.V_K_regler = PI_Regler(Kp = -0.25, Ki = -0.15, dt = self.dt, minimalwert=0, maximalwert=1,antiwindup_lower=0,antiwindup_upper=1, name = "V_K")
        self.V_K_regler = PI_Regler(Kp = -0.125, Ki = -0.075, dt = self.dt, minimalwert=0, maximalwert=1,antiwindup_lower=0,antiwindup_upper=1, name = "V_K")
        
        self.V_F_regler = PI_Regler(Kp = 0.0005, Ki = 0.00005, dt = self.dt, minimalwert=-1, maximalwert=1,antiwindup_lower=-1,antiwindup_upper=1, name = "V_F")
        self.V_F_regler = PI_Regler(Kp = 0.000, Ki = 0.0000, dt = self.dt, minimalwert=0, maximalwert=1,antiwindup_lower=0,antiwindup_upper=1, name = "V_F")


















        #################### init für simulierte anlage
        self.wt_anlage = wärmetauscher(dt=self.dt, startwert=startwert)

        self.tot1_anlage = Transportdelay(n_Bins=1000, volumen=0.001486098988854, startwert=startwert)
        self.tot2_anlage = Transportdelay(n_Bins=1000, volumen=0.005972953032638, startwert=startwert)
        self.tot3_anlage = Transportdelay(n_Bins=1000, volumen=0.003664353671147, startwert=startwert)
        self.tot4_anlage = Transportdelay(n_Bins=1000, volumen=0.020497478347979, startwert=startwert)

        self.rohr1_anlage = rohrstück_1(dt=self.dt, startwert=startwert)
        self.rohr2_anlage = rohrstück_2(dt=self.dt, startwert=startwert)

        self.misch_anlage = mischventil(startwert=startwert)

        
        ############ log init ################
        names = "s,F1, F2, F3, T1, T2, T3, T4, T_D40, T5, T6, TOELE, T_T_1, T_T_2, f, s_k, s_k2, k, s_V, s_V_K, r_tilde, T_BP1, T_BP2, T_WT1, T_WT2, T_V, T_V2, m, r, T_V_tilde"
        with open("log.txt", "w") as file:
            file.write(names + "\n")

    def update(self, input):
        self.zähler += self.dt
        F  = 0.001
        s = 90
        if self.zähler>500:
            s = 85
        if self.zähler>1000:
            s = 80
        if self.zähler>1500:
            s = 75
        if self.zähler>2000:
            s = 70
        if self.zähler>2500:
            s = 65
        if self.zähler>3000:
            s = 60
        if self.zähler>3500:
            s = 85


        #T_D40 = np.array([70])
        T_tank = np.array([90])
        #TOELE = np.array([70])
        T_kuehl = np.array([23])

        ##########  regelstrecke (löschen für implementierung auf Teststand) ##############################################
        [F1, F2, F3] = F_nach_r.update(F=F, r=self.r)
        T1 = self.rohr1_anlage.update(F=F2, input= T_tank)
        T2 = self.tot1_anlage.update(F=F2, input=T1, dt=self.dt)

        T3 = self.wt_anlage.update(F=F3, T_tank=T_tank, T_kuehl=T_kuehl)
        T4 = self.tot2_anlage.update(F=F3, input=T3, dt=self.dt)

        T_D40 = self.misch_anlage.update(F1=F1,F2=F2,F3=F3,T_BP2=T2,T_WT2=T4)
        T_D40 = self.filter_V.update(input=T_D40)

        T5 = self.tot3_anlage.update(F=F1,input=T_D40, dt=self.dt)
        T6 = self.rohr2_anlage.update(F=F1, input=T5)
        TOELE  = self.tot4_anlage.update(F=F1, input=T6, dt=self.dt)
        TOELE = self.filter_T.update(input=TOELE)

        
        ##########  T~  ######################################################
        T_T_1 = self.rohr2.update(F=self.F1, input=T_D40)
        T_T_1 = self.filter_T_tilde.update(input = T_T_1)

        ##########  totzeit T~  ##############################################
        T_T_2 = self.tot4.update(F=self.F1, input=T_T_1, dt=self.dt)
        f = self.F_regler.update(fehler =TOELE-T_T_2)
        s_k = f + s
        s_k2 = s_k-T_T_1
        self.K_regler.set_limits(minimalwert=T_kuehl-s_k , maximalwert=T_tank-s_k,antiwindup_lower=T_kuehl-s_k , antiwindup_upper=T_tank-s_k)
        k = self.K_regler.update(fehler =s_k2)
        s_V = k + s_k
        s_V_K = s_V - self.T_V_tilde
        r_tilde = self.V_K_regler.update(fehler= s_V_K)
        ##########  V~  ######################################################
        [self.F1, self.F2, self.F3] = F_nach_r.update(F=F, r=r_tilde)
        T_BP1 = self.rohr1.update(F=self.F2, input=T_tank)
        T_BP2 = self.tot1.update(F=self.F2, input=T_BP1, dt=self.dt)
        T_WT1 = self.wt.update(F=self.F3, T_tank=T_tank, T_kuehl=T_kuehl)
        T_WT2 = self.tot2.update(F=self.F3, input=T_WT1, dt=self.dt)
        self.T_V_tilde = self.misch.update(F1=self.F1, F2=self.F2, F3=self.F3, T_BP2=T_BP2, T_WT2=T_WT2)
        self.T_V_tilde = 1+self.filter_V_tilde.update(input = self.T_V_tilde)
        ##########  totzeit V~  ##############################################
        T_V = self.tot3.update(F=self.F1, input=self.T_V_tilde, dt=self.dt)
        T_V2 = T_D40 - T_V 

        m = self.V_F_regler.update(fehler= T_V2)
        self.r = m + r_tilde
        ##########  ende smithpredictor  ##############################################

        

        if False:
            print("\n\n\n\n\nSmithpredictor rechnet \tT_V_tilde: {:.2f}\tr_tilde: {:.2f}\t\tT_M: {:.2f}\tT_V2: {:.2f}\ts_V_K: {:.2f}\ts_V: {:.4f}".format(
                float(self.T_V_tilde), float(r_tilde), float(self.T_V_tilde), float(T_V2), float(s_V_K), float(s_V)))
            print("Smithpredictor rechnet \ts: {:.2f}\t\tr: {:.2f}\t\t\tT_D40: {:.2f}\tTOELE: {:.2f}\tT_T_2: {:.2f}\tf: {:.2f}".format(
                float(s), float(self.r), float(T_D40), float(TOELE), float(T_T_2),float(f)))
            print("Smithpredictor rechnet \ts_k2: {:.2f}\t\tk: {:.2f}".format(float(s_k2), float(k)))


        ############ log ################
        string = "{:.2f},{:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}, {:.2f}".format(float(s),float(self.F1), float(self.F2), float(self.F3), float(T1), float(T2), float(T3), float(T4), float(T_D40), float(T5), float(T6), float(TOELE), float(T_T_1), float(T_T_2), float(f), float(s_k), float(s_k2), float(k), float(s_V), float(s_V_K), float(r_tilde), float(T_BP1), float(T_BP2), float(T_WT1), float(T_WT2), float(T_V), float(T_V2), float(m), float(self.r), float(self.T_V_tilde))
        with open("log.txt", "a") as file:
            file.write(string + "\n")

        return self.r
    
  