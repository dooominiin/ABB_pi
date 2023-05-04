from Regler.modelle import Transportdelay

class Smithpredictor:
    def __init__(self,dt):
        self.last_input = 0  # Speichere den letzten Input
        self.last_output = 0  # Speichere den letzten Output
        self.integral = 0  # Speichere den integralen Fehler
        self.dt = dt # diskretisierungszeitschritt
        self.delay = mod.Transportdelay(1000,100,80)
    def update(self, input):
        input_value = self.delay.update(10,input,self.dt)
        error = input_value - self.last_input  # Berechne den Fehler
        self.integral += error  # Addiere den Fehler zum integralen Fehler
        output = 0.5 * error + 0.2 * self.integral + 0.3 * self.last_output  # Berechne den neuen Output
        self.last_input = input_value  # Speichere den aktuellen Input
        self.last_output = output  # Speichere den aktuellen Output
        print("Updating Regler with input: ", input_value)
        return output
        