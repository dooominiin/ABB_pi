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

class VarUpdater(Thread):
    def __init__(self, vars):
        Thread.__init__(self)
        self._stopev = False
        self.vars = vars

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            for var in self.vars:
                v = 70 + sin(time.time() * 5)*20
                var.set_value(v)
                print("Variabel aktualisiert mit: ",var)
            time.sleep(update_intervall)


class OpcUaServer_Monitoring    # create server object
    server = Server()

    # set server name
    server.set_server_name("OPC Server Schmieroeltemperaturregler Monitoring")

    # set endpoint
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace
    uri = "schmieroelregler_monitor"
    idx = server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    device_type = server.nodes.base_object_type.add_object_type(
        idx, "Sensorwerte")


    # create an instance of our device type in the address space
    device = server.nodes.objects.add_object(
        idx, "Temperaturen", objecttype=device_type)

    # node für den client writable machen
    #device.get_child(["{}:r".format(idx)]).set_writable(writable=True)

    # Lade die Variablen aus der JSON-Datei und erstelle sie im OPC-Server
    with open("OPC/variablen.json", "r", encoding='utf-8') as file:
        variables = json.load(file)
        for var_info in variables:
            name = var_info["name"]
            namespace = var_info["namespace"]
            string = var_info["string"]
            type = var_info["type"]
            node_id = ua.NodeId.from_string(f"{namespace};{string}")
            print(node_id)
            if type == "Float":
                var = device.add_variable(node_id, name, ua.Variant(0, ua.VariantType.Float))
            if type == "Int32":
                var = device.add_variable(node_id, name, ua.Variant(0, ua.VariantType.Int32))
            print(var)
            var.set_modelling_rule(True)
            var.set_value(0)
            var.set_writable(writable=var_info["writable"])

    
    # start variable updater thread
    vars = [
        #device.get_child(["{}:T_D40".format(idx)]),
        #device.get_child(["{}:T_tank".format(idx)]),
        #device.get_child(["{}:T_kuehl".format(idx)]),
        #device.get_child(["{}:F".format(idx)]),
        #device.get_child(["{}:s".format(idx)]),
        #device.get_child(["{}:r".format(idx)])
    ]
    var_updater = VarUpdater(vars)
    var_updater.start()

    # start server
    try:
        server.start()
    
        try:
            print("Press Ctrl-C to stop.")
            while True:
                time.sleep(0.1)

        except KeyboardInterrupt:
            pass
  
        finally:
            # stop variable updater thread
            var_updater.stop()

            # stop server
            server.stop()
        
    except:
        # stop variable updater thread
        var_updater.stop()

    # run server until stopped by user

