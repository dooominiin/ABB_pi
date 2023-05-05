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
        print("Python: New data change event", node, val)
        self.regler.set_input(val) # neue daten zum regler schicken

    def event_notification(self, event):
        print("Python: New event", event)



class OpcUaClient:
    def __init__(self, dt):
        self.client = Client("opc.tcp://localhost:4840/freeopcua/server/")
        self.terminate = False
        self.thread = Thread(target=self.loop_forever)
        self.output = 0
        self.input = 0
        self.dt = dt # diskretisierungszeitschritt

    def set_regler_client_reference(self,regler):
        self.regler = regler
        self.regler.set_opc_client(self)
        try:
            self.client.connect()
            root = self.client.get_root_node()
            # meine variabeln
            self.myvar = root.get_child(["0:Objects", "2:Temperaturen", "2:Temperatur Käse"])
            self.myvar2 = root.get_child(["0:Objects", "2:Temperaturen", "2:Temperatur Brot"])
            # subscribing to a variable node
            self.handler = SubHandler()
            self.handler.get_regler(self.regler)
            self.subscription = self.client.create_subscription(500, self.handler)
            self.handle = self.subscription.subscribe_data_change(self.myvar)
        except:
            pass
    
    def set_output(self,output):
        self.output = output

    def loop_start(self):
        self.thread.start()

    def loop_forever(self):
        while not self.terminate:                       
            start_time = time.time()  # Startzeit speichern
            self.input += 1
            
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
  
    def loop_stop(self):
        self.terminate = True
        self.thread.join()
        self.subscription.delete()
        self.client.disconnect()
