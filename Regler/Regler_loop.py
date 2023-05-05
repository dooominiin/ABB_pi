import time
from threading import Thread
from Regler.Smithpredictor import Smithpredictor

class Regler:
    def __init__(self,dt):
        self.terminate = False
        self.thread = Thread(target=self.loop_forever)
        self.input = 0  
        self.output = 0
        self.dt = dt # diskretisierungszeitschritt
        self.client = None
        self.Smithpredictor = Smithpredictor(dt)

    def set_opc_client(self, client):
        self.client = client
    
    def set_input(self,input):
        self.input = input

    def loop_start(self):
        self.thread.start()

    def loop_forever(self):
        while not self.terminate:
            start_time = time.time()  # Startzeit speichern
            ######################## Regler ########################
            self.output = self.Smithpredictor.update(self.input)
            ##################### Regler fertig ####################
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
    
    def loop_stop(self):
        self.terminate = True
        self.thread.join()

    