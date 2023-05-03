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
    def __init__(self, var):
        Thread.__init__(self)
        self._stopev = False
        self.var = var

    def stop(self):
        self._stopev = True

    def run(self):
        while not self._stopev:
            v = sin(time.time() / 10)
            self.var.set_value(v)
            time.sleep(0.1)


if __name__ == "__main__":
    # optional: setup logging
    logging.basicConfig(level=logging.WARN)

    # create server object
    server = Server()

    # set server name
    server.set_server_name("Thomas OPC-UA Server")

    # set endpoint
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # setup our own namespace
    uri = "http://example.com/ThomasOPCUAServer"
    idx = server.register_namespace(uri)

    # create a new node type we can instantiate in our address space
    device_type = server.nodes.base_object_type.add_object_type(
        idx, "MyDeviceType")

    # add variable to device type
    device_type.add_variable(
        idx, "thomas", ua.Variant(0, ua.VariantType.Float)).set_modelling_rule(True)

    # create an instance of our device type in the address space
    device = server.nodes.objects.add_object(
        idx, "Device0001", objecttype=device_type)

    # start variable updater thread
    var_updater = VarUpdater(device.get_child(["{}:thomas".format(idx)]))
    var_updater.start()

    # start server
    server.start()

    # run server until stopped by user
    try:
        print("Press Ctrl-C to stop.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        # stop variable updater thread
        var_updater.stop()

        # stop server
        server.stop()
