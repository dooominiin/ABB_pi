import time
from threading import Thread
from Regler.Smithpredictor import Smithpredictor
import json
from enum import Enum
from Monitor.ueberwachung import Monitor

# Die Reglerklasse führt den Smithpredictor Regler aus, führt INPUT und OUTPUT mit Regler und OPC-Client zusammen und enthält die Ablääufe für die verschiedenen Betriebszustände des Reglers. 

class Regler:
    def __init__(self,dt,server):
        self.terminate = False
        self.running = True
        self.thread = Thread(target=self.loop_forever)

        # JSON laden und Namen auslesen
        with open("OPC/variablen.json", "r", encoding='utf-8') as file:
            
            variables = json.load(file)
            
            variable_names = [var_info["name"] for var_info in variables]
        # Input-Liste initialisieren
        self.input = {name: 60.0 if name.startswith("T") else 0.0 for name in variable_names}

        self.output = self.input.copy()

        self.dt = dt # diskretisierungszeitschritt
        self.dt_alt = dt
        self.client = None
        self.Smithpredictor = Smithpredictor(dt)
        self.monitor = Monitor(server=server)


    def set_opc_client(self, client):
        self.client = client
    
 

    def set_input(self, input, node):
        with open("OPC/variablen.json", "r", encoding='utf-8') as file:
            variables = json.load(file)
            for var_info in variables:
                name = var_info["name"]
                namespace = var_info["namespace"]
                string = var_info["string"]
                if node == self.client.client.get_node(f"{namespace};{string}"):
                    self.input[name] = input
                    #print(f"Variabel {name} aktualisiert mit dem Wert: {input}")


       
    def loop_start(self):
        if not self.terminate:
            self.thread.start()

    def loop_forever(self):
        
        class Zustand(Enum):
            manueller_Betrieb = 0
            geregelter_Betrieb = 1
            beschleunigt = 2

        while not self.terminate:
            start_time = time.time()  # Startzeit speichern
            ######################## Regler ########################
            if Zustand.geregelter_Betrieb == Zustand(self.input["state"]):
                self.dt = self.dt_alt
                self.output = self.Smithpredictor.update(self.input)
            if Zustand.manueller_Betrieb == Zustand(self.input["state"]):
                self.dt = self.dt_alt
                self.input["s"] = self.input["TOELE"]
                self.output = self.Smithpredictor.update(self.input)
            if Zustand.beschleunigt == Zustand(self.input["state"]):
                self.dt = 0   
                self.output = self.Smithpredictor.update(self.input)
            time_regler = time.time()
            ##################### Regler fertig, opc variablen update ####################
            self.client.set_output(output = self.output)
            time_opc_client = time.time()
            ######################Monitoring über OPC################
            if self.monitor.step(self.dt):
                alle_states = self.Smithpredictor.getAllStates()
                self.monitor.update(alle_states)
                print("Werte für Monitor Server aktualisiert!")
            time_opc_server = time.time()
            
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
            
            print("Regler: {:.4f}\tOPC Client: {:.4f}\tOPC Server: {:.4f}".format(time_regler-start_time,time_opc_client-time_regler, time_opc_server-time_opc_client))

            print(Zustand(self.input["state"]),f"benötigte zeit: {elapsed_time*1000:3.2f} ms")



    def loop_stop(self):
        self.terminate = True
        try:
            self.thread.join()
        except:
            pass
        self.running = False

    def is_running(self):
        return self.running
        