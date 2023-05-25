from threading import Thread
import time
from opcua import Client, ua
import json

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
        self.terminate = False
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
            
            # Lade die Variablen aus der JSON-Datei und erstelle sie im OPC-Server
            with open("OPC/variablen.json", "r") as file:
                variables = json.load(file)
                for var_info in variables:
                    name = var_info["name"]
                    namespace = var_info["namespace"]
                    string = var_info["string"]

                    if var_info["subscribe"]:
                        node=self.client.get_node(nodeid=f"{namespace};{string}")
                        print(node)
                        #myvar = root.get_child(f"{namespace};{string}")
                        #self.handle = self.subscription.subscribe_data_change(node_id)
        except Exception as e:
            print("subscribe der Variabeln nicht möglich!")
            print(e)
            self.terminate = True

    
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
        