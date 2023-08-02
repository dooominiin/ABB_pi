import uuid
from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys
import json

from opcua.ua import NodeId, NodeIdType
from opcua import ua, uamethod, Server

update_intervall = 2; # Zeitintervall, in dem die variabeln im server upgedatet werden.


class OpcUaServer_Monitoring:    # create server object
    def __init(self,dt):

        self.terminate = False
        self.running = True
        self.thread = Thread(target=self.loop_forever)
        self.dt = dt
        self.server = Server()
        # set server name
        self.server.set_server_name("OPC Server Schmieroeltemperaturregler Monitoring")
        # set endpoint
        self.server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
        # setup our own namespace
        uri = "schmieroelregler_monitor"
        idx = self.server.register_namespace(uri)
        # create a new node type we can instantiate in our address space
        device_type = self.server.nodes.base_object_type.add_object_type(
            idx, "States Regler")
        # create an instance of our device type in the address space
        device = self.server.nodes.objects.add_object(
            idx, "Werte", objecttype=device_type)
        self.states_monitoring = {
                'F1': 0,
                'F2': 0,
                'F3': 0,
                'T1': 0,
                'T2': 0,
                'T3': 0,
                'T4': 0,
                'T_D40': 0,
                'T5': 0,
                'T6': 0,
                'TOELE': 0,
                'T_T_1': 0,
                'T_T_2': 0,
                'f': 0,
                's_k': 0,
                's_k2': 0,
                's_V': 0,
                's_V_K': 0,
                'r_tilde': 0,
                'T_BP1': 0,
                'T_BP2': 0,
                'T_WT1': 0,
                'T_WT2': 0,
                'T_V_tilde': 0,
                'T_V': 0,
                'T_V2': 0,
                'm': 0,
                'r_alt': 0,
                'r': 0,
                'F_nach_r': 0,
                'T_tank': 0,
                'T_kuehl': 0,
                # Füge hier weitere Schlüssel hinzu, falls benötigt
            }
            
        # Lade die Variablen aus der JSON-Datei und erstelle sie im OPC-Server
        with open("OPC/variablen_monitoring.json", "r", encoding='utf-8') as file:
            self.variables = json.load(file)
            
        for var_info in self.variables:
            name = var_info["name"]
            namespace = var_info["namespace"]
            string = var_info["string"]
            type = var_info["type"]
            node_id = ua.NodeId.from_string(f"{namespace};{string}")
            if type == "Float":
                var = device.add_variable(node_id, name, ua.Variant(0, ua.VariantType.Float))
            if type == "Int32":
                var = device.add_variable(node_id, name, ua.Variant(0, ua.VariantType.Int32))
            print(var)
            var.set_modelling_rule(True)
            var.set_value(0)
            var.set_writable(writable=var_info["writable"])
        # start server
        try:
            self.server.start()
            self.loop_start()
        except:
            print("Server starten nicht möglich!")
            self.terminate = True
        
    def update(self,states):
        for var_info in self.variables:
            name = var_info["name"]
            namespace = var_info["namespace"]
            string = var_info["string"]
            #node_id = ua.NodeId.from_string(f"{namespace};{string}")
            var = self.server.get_node(f"{namespace};{string}")
            var.set_value(float(states[name]))

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
        
    