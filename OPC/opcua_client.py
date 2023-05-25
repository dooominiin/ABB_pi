from threading import Thread
import time
from opcua import Client

class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """
    def get_regler(self,regler):
        self.regler = regler

    def datachange_notification(self, node, val, data):
        #print("Python: New data change event", node, val)
    
        self.regler.set_input(val,node) # neue daten zum regler schicken

    def event_notification(self, event):
        print("Python: New event", event)



class OpcUaClient:
    def __init__(self, dt, regler):
        self.client = Client("opc.tcp://localhost:4840/freeopcua/server/")
        self.client = Client("opc.tcp://192.168.43.97:4840/freeopcua/server/")  # adresse lenovo hotspot
        try:
            self.client.connect()
            root = self.client.get_root_node()
        except:
            print("Verbindung zum OPC Server nicht möglich!")
        self.terminate = False
        self.thread = Thread(target=self.loop_forever)
        self.output = 0
        self.dt = dt # diskretisierungszeitschritt
        
        
        self.regler = regler
        self.regler.set_opc_client(self)

        try:            
            # subscribing to a variable node
            self.handler = SubHandler()
            self.handler.get_regler(self.regler)
            self.subscription = self.client.create_subscription(500, self.handler) 
            
            # meine variabeln
            variable_names = ["T_D40", "T_tank", "T_kuehl", "F", "s", "r"]
            for var_name in variable_names:
                myvar = root.get_child(["0:Objects", "2:Temperaturen",f"2:{var_name}"])
                self.handle = self.subscription.subscribe_data_change(myvar)
        except:
            print("subscribe der Variabeln nicht möglich!")

    
    def set_output(self,output):
        self.output = output

    def loop_start(self):
        self.thread.start()

    def loop_forever(self):
        while not self.terminate:                       
            start_time = time.time()  # Startzeit speichern
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
  
    def loop_stop(self):
        self.terminate = True
        self.thread.join()
        if hasattr(self.client, 'subscription'):
            self.client.subscription.delete()
        self.client.disconnect()
        