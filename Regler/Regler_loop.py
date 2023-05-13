import time
from threading import Thread
from Regler.Smithpredictor import Smithpredictor
import numpy as np
import os

class Regler:
    def __init__(self,dt):
        self.terminate = False
        self.thread = Thread(target=self.loop_forever)

        self.input = {
            "T_D40": 60,
            "T_tank": 60,
            "T_t": 60,
            "F": 0.001,
            "s": 0,
            "r": 0.5
        }
        self.output = 0
        self.dt = dt # diskretisierungszeitschritt
        self.client = None
        self.Smithpredictor = Smithpredictor(dt)

    def set_opc_client(self, client):
        self.client = client
    
    def set_input(self, input, node):
        if node == self.client.client.get_node("ns=2;i=9"):
            self.input["T_D40"] = input
            #print(f"Variable T_D40 aktualisiert mit dem Wert: {input}")
        elif node == self.client.client.get_node("ns=2;i=10"):
            self.input["T_tank"] = input
            #print(f"Variable T_tank aktualisiert mit dem Wert: {input}")
        elif node == self.client.client.get_node("ns=2;i=11"):
            self.input["T_t"] = input
            #print(f"Variable T_t aktualisiert mit dem Wert: {input}")
        elif node == self.client.client.get_node("ns=2;i=12"):
            self.input["F"] = input
            #print(f"Variable F aktualisiert mit dem Wert: {input}")
        elif node == self.client.client.get_node("ns=2;i=13"):
            self.input["s"] = input
            #print(f"Variable s aktualisiert mit dem Wert: {input}")
        elif node == self.client.client.get_node("ns=2;i=14"):
            self.input["r"] = input
            #print(f"Variable r aktualisiert mit dem Wert: {input}")

       
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
            #print("benötigte zeit: ",elapsed_time)

    def loop_stop(self):
        self.terminate = True
        self.thread.join()

    