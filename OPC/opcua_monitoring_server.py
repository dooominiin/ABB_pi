from threading import Thread
import time
import json
from Monitor.ueberwachung import Monitor
from opcua import ua, Server

# Dieser OPCUA-Server ist dafür gedacht, die inneren Zustände des Reglers nach aussen sichtbar zu machen. Er ist read-only! So kann über ein externes Gerät wie ein Laptob der Zustand des Reglers überwacht werden. Dafür muss man einfach im gleichen Netzwerk wie das Raspberry Pi sein und auf den gleichen Port zugreifen. 

class OpcUaServer_Monitoring:    # create server object
    def __init__(self,aktualisierungsintervall):
        self.intervall = aktualisierungsintervall
        self.terminate = False
        self.running = True
        self.thread = Thread(target=self.loop_forever)
        self.dt = 0.1
        self.server = Server()
        # set server name
        self.server.set_server_name("OPC Server Schmieroeltemperaturregler Monitoring")
        # set endpoint
        self.server.set_endpoint("opc.tcp://0.0.0.0:4841/freeopcua/server/")
        # setup our own namespace
        uri = "schmieroelregler_monitor"
        idx = self.server.register_namespace(uri)
        # create a new node type we can instantiate in our address space
        device_type = self.server.nodes.base_object_type.add_object_type(
            idx, "States Regler")
        # create an instance of our device type in the address space
        device = self.server.nodes.objects.add_object(
            idx, "Werte", objecttype=device_type)
        self.states_monitoring = Monitor.states_dictionary()

        # Lade die Variablen aus der JSON-Datei und erstelle sie im OPC-Server
        with open("OPC/variablen_monitoring.json", "r", encoding='utf-8') as file:
            self.variables = json.load(file)

        for var_info in self.variables:
            name = var_info["name"]
            namespace = var_info["namespace"]
            string = "{}//{}".format(var_info["string"],name)
            type = var_info["type"]
            node_id = ua.NodeId.from_string(f"{namespace};{string}")
            if type == "Float":
                var = device.add_variable(node_id, name, ua.Variant(0, ua.VariantType.Float))
            if type == "Int32":
                var = device.add_variable(node_id, name, ua.Variant(0, ua.VariantType.Int32))
            var.set_modelling_rule(True)
            var.set_value(0)
            var.set_writable(writable=var_info["writable"])

        # start server
        try:
            self.server.start()
            print("Starten des OPC-Monitoring Servers erfolgreich")
        except Exception as e:
            print("Server starten nicht möglich!")
            print(e)
            self.terminate = True
        self.loop_start()
    
    def update(self,states):
        #print(states)
        for var_info in self.variables:
            name = var_info["name"]
            namespace = var_info["namespace"]
            string = "{}//{}".format(var_info["string"],name)
            #node_id = ua.NodeId.from_string(f"{namespace};{string}")
            var = self.server.get_node(f"{namespace};{string}")
            #print(var)
            var.set_value(float(states[name]))
    
    def get_intervall(self):
        return self.intervall
    
    def loop_start(self):
        if not self.terminate:
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
            if hasattr(self.server, 'subscription'):
                self.server.subscription.delete()
        except:
            pass
        try:
            self.server.stop()
        except:
            pass
        self.running = False

    def is_running(self):
        return self.running
        
    