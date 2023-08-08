from threading import Thread
import time
from opcua import Client, ua
import json
from datetime import datetime

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
    def get_monitor(self,monitor):
        self.monitor = monitor

    def datachange_notification(self, node, val, data):
        #print("Python: New data change event", node, val)
        #self.monitor.set_input(val,node) # neue daten zum monitorprogramm schicken
        print("subscribed variabel {} wurde getriggert. {}".format(node,datetime.now().time()))

    def event_notification(self, event):
        print("Python: New event", event)



class OpcUaClient:
    def __init__(self, dt):
        self.dt = dt # diskretisierungszeitschritt
        self.zähler = 0                
        self.client = Client("opc.tcp://192.168.43.203:4842/freeopcua/server/")  # adresse lenovo handy hotspot
        self.terminate = False
        self.running = False
        self.thread = Thread(target=self.loop_forever)
        zähler = 0
        while not self.terminate:
            try:
                self.client.connect()
                print("Verbindung zum OPC Server erfolgreich")
                break
            except:
                print(f"Verbindung zum OPC Server nicht möglich! {zähler+1}er Versuch!")
                zähler += 1
                if zähler >= 5:
                    print(f"Abbruch nach {zähler} Versuchen!")
                    self.terminate = True
                    self.running = False
        if not self.terminate:
            # subscribing to a variable node
            self.handler = SubHandler()
            #self.handler.get_regler(self.regler)
            self.subscription = self.client.create_subscription(500, self.handler) 

            try:    
                # Lade die Variablen aus der JSON-Datei und erstelle sie im OPC-Server
                with open("OPC/variablen_monitoring.json", "r", encoding='utf-8') as file:
                    variables = json.load(file)
                    for var_info in variables:
                        name = var_info["name"]
                        namespace = var_info["namespace"]
                        string = "{}//{}".format(var_info["string"],name)
                        if var_info["subscribe"]:
                            try:            
                                node=self.client.get_node(nodeid=f"{namespace};{string}")
                                self.handle = self.subscription.subscribe_data_change(node)
                                print("subscribed to: ",name)

                            except Exception as e:
                                print("subscribe der Variabel {} nicht möglich! name: >>{}<<name   string: {}".format(node, name, string))
                                print(e)
                                self.terminate = True
                                raise
            except:
                print("subscriben aller variabeln fehlgeschlagen!")
                self.loop_stop()
            else:
                self.loop_start()
                print("Thread gestartet")
    
    def set_output(self,output):
        if not self.am_senden:
            self.output = output
         
    def send(self):
        self.zähler += self.dt
        if self.zähler >= self.output_update_intervall:
            t1 = time.time()
            with open("OPC/variablen_monitoring.json", "r", encoding='utf-8') as file:
                variables = json.load(file)
            self.am_senden = True
            for var_info in variables:
                name = var_info["name"]
                namespace = var_info["namespace"]
                string = var_info["string"]
                if var_info["is_output"]:
                    #print("update output",name,float(self.output[name]))
                    time_1=time.time()
                    self.client.get_node(f"{namespace};{string}").set_value(float(self.output[name]))
            t2 = time.time()
            #print("output wurde gesendet in {:.4f} s".format(t2-t1))
            self.am_senden = False
            self.zähler = 0

        

    def loop_start(self):
        if not self.terminate:
            self.running = True
            self.thread.start()

    def loop_forever(self):
        while not self.terminate:                       
            start_time = time.time()  # Startzeit speichern
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
  
    def loop_stop(self):
        self.terminate = True
        try:
            self.thread.join()
        except Exception as e:
            print(e)
            pass    
        try:
            if hasattr(self.client, 'subscription'):
                self.client.subscription.delete()
        except Exception as e:
            print(e)
            pass
        try:    
            self.client.disconnect()
        except Exception as e:
            print(e)
            pass
        self.running = False

    def is_running(self):
        return self.running
    
if __name__ == "__main__":
    c = OpcUaClient(0.1)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        c.loop_stop()
    