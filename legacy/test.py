import time
import sys
sys.path.insert(0, "..")
from opcua import Client
from opcua import ua
from threading import Thread

class Regler:

    def __init__(self):
        self._t = 0

    def doit(self):
        pass

    def update_t(self, var):


    def set_opc_client(self, client):

        pass

    def loop(self):
        while True:
            time.sleep(1)
            self._t
            print("Gugus")


class ReglerOpcUaClient:
    def __init__(self, regler):
        self._terminate = False
        self._thread = Thread(target=self.loop_forever)
        self._regler = regler

        regler.set_opc_client(self)


    def loop_start(self):

        self._thread.start()

    def loop_forever(self):
        
        while not self._terminate:
            time.sleep(1)
            self._regler.update_t(25)
            print("opc tut was")

    def loop_stop(self):
        self._terminate = True

        self._thread.join()



class SubHandler(object):

    """
    Subscription Handler. To receive events from server for a subscription
    data_change and event methods are called directly from receiving thread.
    Do not do expensive, slow or network operation there. Create another 
    thread if you need to do such a thing
    """

    def datachange_notification(self, node, val, data):
        print("Python: New data change event", node, val)

    def event_notification(self, event):
        print("Python: New event", event)


if __name__ == "__main__":
  
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    # client = Client("opc.tcp://admin@localhost:4840/freeopcua/server/") #connect using a user
    try:
        client.connect()
        client.load_type_definitions()  # load definition of server specific structures/extension objects

        # Client has a few methods to get proxy to UA nodes that should always be in address space such as Root or Objects
        root = client.get_root_node()
        print("Root node is: ", root)
        objects = client.get_objects_node()
        print("Objects node is: ", objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        print("Children of root are: ", root.get_children())

        # gettting our namespace idx
        uri = "http://examples.freeopcua.github.io"
        idx = client.get_namespace_index(uri)

        # Now getting a variable node using its browse path
        myvar = root.get_child(["0:Objects", "{}:MyObject".format(idx), "{}:MyVariable".format(idx)])
        obj = root.get_child(["0:Objects", "{}:MyObject".format(idx)])
        print("myvar is: ", myvar)

        # subscribing to a variable node
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(myvar)
        time.sleep(0.1)

        # we can also subscribe to events from server
        sub.subscribe_events()
        # sub.unsubscribe(handle)
        # sub.delete()

        # calling a method on server
        res = obj.call_method("{}:multiply".format(idx), 3, "klk")
        print("method result is: ", res)

        embed()
    finally:
        client.disconnect()




if __name__ == "__main__":
    
    
    r = Regler()
    c = ReglerOpcUaClient(r)

    try:
        c.start()
        r.loop_forever()
    except (SystemExit, KeyboardInterrupt) as e:
        c.stop()
        r.stop()


