from Regler.modelle import Transportdelay
# Implementiert einen Smithpredicter, der die eigentliche regelung vornimmt. 

class Smithpredictor:
    def __init__(self,dt):
        self.dt = dt
        self.delay = Transportdelay(n_Bins=1000,volumen=100,startwert=80)
        

    def update(self,input):
        output = self.delay.update(F=10,eingangstemperatur=input,dt=self.dt)
        print("Smithpredictor rechnet ",output)
        return output
    
