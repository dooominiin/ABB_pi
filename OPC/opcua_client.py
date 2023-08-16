from threading import Thread
import time
from opcua import Client, ua
import json
import logging

# Der OPCUA-Client stellt die verbindung zum Leitsystem dar und handelt 
# INPUT und OUTPUT des Reglers. Das OPCUA Protokoll stellt eine Public 
# Subscriber Struktur zur verfügung. Das bedeuted, dass der CLient beim 
# Leitsystem bei den Sensorwerten "subscribed" und dann benachrichtigt 
# wird, wenn neue Werte vorliegen. Die Variabeln zum werden über das 
# variabeln.json File verwaltet. 

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
       #print("Python: New event", event)
       pass



class OpcUaClient:
    def __init__(self, dt, regler,output_update_intervall):
        self.output_update_intervall = output_update_intervall
        self.zähler = 0                
        self.am_senden = False
        self.client = Client("opc.tcp://localhost:4840/freeopcua/server/")
        self.client = Client("opcda://172.16.4.21/ABB.AfwOpcDaSurrogate.1") # 800xa surrogate
        self.client = Client("opcda://PRIOPC1/ABB.AfwOpcDaSurrogate.1") # 800xa surrogate
        self.client = Client("opc.tcp://172.16.4.150:48050/") # UA gateway
        self.client = Client("opc.tcp://192.168.43.97:4840/freeopcua/server/")  # adresse lenovo handy hotspot
        self.client = Client("opc.tcp://192.168.43.6:4840/freeopcua/server/")  # adresse PC handy hotspot
        


        self.client.timeout = 10  # Setze den Standard-Timeout auf 10 Sekunden
        self.client.uarequest_timeout = 5  # Setze den Timeout für UA-Anfragen auf 5 Sekunden

        
        self.terminate = False
        self.running = True
        zähler = 0
        while not self.terminate:
            try:
                self.client.connect()
                print("Verbindung zum OPC Server erfolgreich")
                break
            except Exception as e:
                print(f"Verbindung zum OPC Server nicht möglich! {zähler+1}er Versuch!")
               #print(e)
                zähler += 1
                if zähler >= 5:
                    print(f"Abbruch nach {zähler} Versuchen!")
                    self.terminate = True
                    self.running = False

        self.thread = Thread(target=self.loop_forever)
        self.output = 0
        self.dt = dt # diskretisierungszeitschritt
        
        
        self.regler = regler
        self.regler.set_opc_client(self)
        if self.terminate:
            self.regler.loop_stop()
            print("Regler gestoppt durch Client")
        else:
            try:            
                # subscribing to a variable node
                self.handler = SubHandler()
                self.handler.get_regler(self.regler)
                self.subscription = self.client.create_subscription(500, self.handler) 
                
                # Lade die Variablen aus der JSON-Datei und erstelle sie im OPC-Server
                with open("OPC/variablen.json", "r", encoding='utf-8') as file:
                    variables = json.load(file)
                    for var_info in variables:
                        name = var_info["name"]
                        namespace = var_info["namespace"]
                        string = var_info["string"]
                        if var_info["subscribe"]:
                            node=self.client.get_node(nodeid=f"{namespace};{string}")
                            self.handle = self.subscription.subscribe_data_change(node)
                            print("subscribed to: ",name)

            except Exception as e:
                print("subscribe der Variabel {} nicht möglich!".format(name))
                print(e)
                self.terminate = True

    
    def set_output(self,output):
        if not self.am_senden:
            self.output = output
         
    def send(self):
        self.zähler += self.dt
        if self.zähler >= self.output_update_intervall:
            t1 = time.time()
            with open("OPC/variablen.json", "r", encoding='utf-8') as file:
                variables = json.load(file)
            self.am_senden = True
            for var_info in variables:
                name = var_info["name"]
                namespace = var_info["namespace"]
                string = var_info["string"]
                if var_info["is_output"]:
                    #print("update output",name,float(self.output[name]))
                    time_1=time.time()
                    try:
                        try:
                            my_node = self.client.get_node(f"{namespace};{string}")
                            #print("get_node() gelungen mit :{}".format(my_node))
                        except Exception as e:
                            print("Versuchte get_node() mit {}".format(string))
                            print(e)
                            self.terminate = True
                            raise
                        try:
                            #var = my_node.get_data_value()
                            #my_node.set_data_value(var)
                            my_node.set_value(float(self.output[name]))
                            #print("set_value() gelungen mit :{}".format(my_node))
                        except Exception as e:
                            print("Versuchte set_value() mit {}".format(my_node))
                            print(e)
                            self.terminate = True
                            raise
                    except:
                        pass

            t2 = time.time()
            #print("output wurde gesendet in {:.4f} s".format(t2-t1))
            self.am_senden = False
            self.zähler = 0

        
    def loop_start(self):
        if not self.terminate:
            self.thread.start()

    def loop_forever(self):
        while True:                       
            start_time = time.time()  # Startzeit speichern
            self.send()
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
            if self.terminate:
                self.loop_stop()
                break

    def loop_stop(self):
        self.terminate = True
        try:
            self.thread.join()
        except Exception as e:
            print(e)
                
        try:
            if hasattr(self.client, 'subscription'):
                self.client.subscription.delete()
        except Exception as e:
            print(e)
            
        try:    
            self.client.disconnect()
        except Exception as e:
            print(e)
            
        self.running = False

    def is_running(self):
        return self.running
        