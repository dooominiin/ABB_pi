from Regler.modelle import Transportdelay
from Regler.modelle import transportdelay
from Regler.modelle import rohrstueck
import control as ct
import numpy as np

# Implementiert einen Smithpredicter, der die eigentliche regelung vornimmt. 


class Smithpredictor:
    def __init__(self,dt):
        self.dt = dt
        self.delay = Transportdelay(n_Bins=1000,volumen=100,startwert=80)
        self.trans = transportdelay(dt=self.dt, n_Bins=1000, volumen=100)
        self.rohr = rohrstueck(dt = self.dt)        
        self.seriell = ct.series(self.trans,self.rohr)


    def update(self,input):
        output = self.delay.update(F=10,eingangstemperatur=input,dt=self.dt)
        x = self.trans.x
        print(x)
        #output = self.trans.dynamics(t=self.dt,u=input)
        print("Smithpredictor rechnet ",output)
        return output
    
