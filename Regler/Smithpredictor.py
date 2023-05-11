from Regler.modelle import Transportdelay
from Regler.modelle import rohrstück_1
from Regler.modelle import rohrstück_2
from Regler.modelle import wärmetauscher
from Regler.modelle import F_nach_r
from Regler.modelle import mischventil
from Regler.modelle import PIDRegler
import numpy as np

# Implementiert einen Smithpredicter, der die eigentliche regelung vornimmt. 


class Smithpredictor:
    def __init__(self, dt):
        self.dt = dt
        startwert = 70
        self.r = 0.5
        self.s = 60

        self.wt = wärmetauscher(dt=self.dt, startwert=startwert)
    
        self.tot1 = Transportdelay(n_Bins=1000, volumen=0.001486098988854, startwert=startwert)
        self.tot2 = Transportdelay(n_Bins=1000, volumen=0.005972953032638, startwert=startwert)
        self.tot3 = Transportdelay(n_Bins=1000, volumen=0.003664353671147, startwert=startwert)
        self.tot4 = Transportdelay(n_Bins=1000, volumen=0.020497478347979, startwert=startwert)

        self.rohr1 = rohrstück_1(dt=self.dt, startwert=startwert)
        self.rohr2 = rohrstück_2(dt=self.dt, startwert=startwert)

        self.misch = mischventil(startwert=startwert)    

        self.T_tank = np.array([100])

        self.pid = PIDRegler(Kp = 0.01, Ki = 0.01, Kd = 0 , dt = self.dt)


    def update(self, input):
        F  = 0.001#np.abs(input["F"])
        r = np.abs(input["r"])
        s = self.s#input["s"]

        self.T_tank = np.array([90])#np.abs(np.array([input["T_tank"]]))


        [F1, F2, F3] = F_nach_r.update(F=F, r=self.r)

        T_BP1 = self.rohr1.update(F=F2, input=self.T_tank)
        T_BP2 = self.tot1.update(F=F2, input=T_BP1, dt=self.dt)

        T_WT1 = self.wt.update(F=F3, T_tank=self.T_tank, T_kuehl=np.array([20]))
        T_WT2 = self.tot2.update(F=F3, input=T_WT1, dt=self.dt)

        T_M = self.misch.update(F1=F1, F2=F2, F3=F3, T_BP2=T_BP2, T_WT2=T_WT2)
        
        T_D40 = self.tot3.update(F=F1, input=T_M, dt=self.dt)
        T_T_1 = self.rohr2.update(F=F1, input=T_D40)
        T_T_2 = self.tot4.update(F=F1, input=T_T_1, dt=self.dt)

        e = s-T_M
        self.r = self.pid.update(fehler = e)

        # Rest des Codes
        print("Smithpredictor rechnet \t\ts: {:.2f}\tr: {:.2f}\t\tT_M: {:.2f}\tinput: {:.2f}\tT_WT1: {:.2f}\tF3: {:.4f}".format(
            float(self.s), float(self.r), float(T_M), float(self.T_tank), float(T_WT1), float(F3)))
        
        return T_T_2
    

