import sys
import time 

from opcua import Client

if __name__ == "__main__":
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    try:
        client.connect()

        root = client.get_root_node()
        print("Objects node is: ", root)
        print("Children of root are: ", root.get_children())

        myvar = root.get_child(["0:Objects", "2:Temperaturen", "2:Temperatur Käse"])
        myvar2 = root.get_child(["0:Objects", "2:Temperaturen", "2:Temperatur Brot"])
        obj = root.get_child(["0:Objects", "2:Temperaturen"])
        print("myvar is: ", myvar)
        print("myvar2 is: ", myvar2)
        print("myobj is: ", obj)

   # get a specific node knowing its node id
        var = client.get_node("ns=2;i=5")
        Input_nodes = {var, myvar, myvar2}
        Output_nodes = {myvar2}
        i=99
        while True:
            time.sleep(0.3)
            for node in Input_nodes:
                print(node)
                print(node.get_value())

            for node in Output_nodes:
                print(node)
                print(node.get_value())
                node.set_value(i)
                i=i*-1
                print(node.get_value())

    except KeyboardInterrupt:
        pass

    finally:
        client.disconnect()
