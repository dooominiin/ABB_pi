import sys
import time 

from opcua import Client

# Anzupassen:
# Serveradresse für client
# 
if __name__ == "__main__":
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    try:
        client.connect()

        root = client.get_root_node()
        print("Objects node is: ", root)

        print("Children of root are: ", root.get_children())

        myvar = root.get_child(["0:Objects", "2:Temperaturen", "2:Temperatur Käse"])
        obj = root.get_child(["0:Objects", "2:Temperaturen"])
        print("myvar is: ", myvar)
        print("myobj is: ", obj)

   # get a specific node knowing its node id
        var = client.get_node("ns=2;i=4")
        while True:
            time.sleep(0.3)
            print(var)
            print(var.get_value())

    except KeyboardInterrupt:
        pass

    finally:
        client.disconnect()
