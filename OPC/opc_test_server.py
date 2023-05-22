import uuid
from threading import Thread
import copy
import logging
from datetime import datetime
import time
from math import sin
import sys

from opcua.ua import NodeId, NodeIdType
from opcua import ua, uamethod, Server


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
            time.sleep(5)


if __name__ == "__main__":
    # create server object
    server = Server()

    # set server name
    server.set_server_name("Mein OPC Testserver")

    # set endpoint
    server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")

    # setup our own namespace
    uri = "Mein_OPCUA_Testserver"
    idx = server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    device_type = server.nodes.base_object_type.add_object_type(
        idx, "Sensorwerte")

    # add variable to device type
    device_type.add_variable(
        idx, "T_D40", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)
    device_type.add_variable(
        idx, "T_tank", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)
    device_type.add_variable(
        idx, "T_kuehl", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)
    device_type.add_variable(
        idx, "F", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)
    device_type.add_variable(
        idx, "s", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)
    device_type.add_variable(
        idx, "r", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)


    # create an instance of our device type in the address space
    device = server.nodes.objects.add_object(
        idx, "Temperaturen", objecttype=device_type)

    # node für den client writable machen
    device.get_child(["{}:r".format(idx)]).set_writable(writable=True)

    # start variable updater thread
    vars = [
        #device.get_child(["{}:T_D40".format(idx)]),
        #device.get_child(["{}:T_tank".format(idx)]),
        #device.get_child(["{}:T_kuehl".format(idx)]),
        #device.get_child(["{}:F".format(idx)]),
        device.get_child(["{}:s".format(idx)]),
        #device.get_child(["{}:r".format(idx)])
    ]
    var_updater = VarUpdater(vars)
    var_updater.start()

    # start server
    server.start()

    # run server until stopped by user
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
