from threading import Thread
import time
import asyncio
import json
from asyncua import Client
import logging

# Der OPCUA-Client stellt die verbindung zum Leitsystem dar und handelt INPUT und OUTPUT des Reglers. Das OPCUA Protokoll stellt eine Public Subscriber Struktur zur verfügung. Das bedeuted, dass der CLient beim Leitsystem bei den Sensorwerten "subscribed" und dann benachrichtigt wird, wenn neue Werte vorliegen. Die Variabeln zum werden über das variabeln.json File verwaltet. 

_logger = logging.getLogger(__name__)


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


async def main():
    url = "opc.tcp://localhost:4840/freeopcua/server/"
    #url = "opc.tcp://192.168.43.97:4840/freeopcua/server/"# adresse lenovo hotspot

    async with Client(url=url) as client:
        _logger.info("Root node is: %r", client.nodes.root)
        _logger.info("Objects node is: %r", client.nodes.objects)

        # Node objects have methods to read and write node attributes as well as browse or populate address space
        _logger.info("Children of root are: %r", await client.nodes.root.get_children())


       
        # get a specific node knowing its node id
        #var = client.get_node(ua.NodeId(1002, 2))
        var = client.get_node("ns=5;s=Root//Control Network//TLP//Applications//Mönch//Control Modules//Mönch//Schmierölsystem//M_kuehl:IO.In.Value")
        print(var)
        #await var.read_data_value() # get value of node as a DataValue object
        value =  (var.read_value()) # get value of node as a python builtin
        print(value)
        #await var.write_value(ua.Variant([23], ua.VariantType.Int64)) #set node value using explicit data type
        #await var.write_value(3.9) # set node value using implicit data type

        # Now getting a variable node using its browse path
        #myvar = await client.nodes.root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
        #obj = await client.nodes.root.get_child(["0:Objects", "2:MyObject"])
        #_logger.info("myvar is: %r", myvar)

        # subscribing to a variable node
        #handler = SubHandler()
        #sub = await client.create_subscription(10, handler)
        #handle = await sub.subscribe_data_change(myvar)
        #await asyncio.sleep(0.1)

        # we can also subscribe to events from server
        #await sub.subscribe_events()
        # await sub.unsubscribe(handle)
        # await sub.delete()

        # calling a method on server
        #res = await obj.call_method("2:multiply", 3, "klk")
        #_logger.info("method result is: %r", res)
        while True:
            await asyncio.sleep(1)
            value =  await (var.read_value()) # get value of node as a python builtin
            print(value)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
