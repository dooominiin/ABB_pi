import sys
import time 

from opcua import Client

# Anzupassen:
# Serveradresse für client
# Öl Temperatur Turbine Eingang

if __name__ == "__main__":
    client = Client("opc.tcp://172.16.4.150:48050")
    try:
        client.connect()

        root = client.get_root_node()
        print("Objects node is: ", root)
        print("Children of root are: ", root.get_children())

    # get specific nodes knowing the node id
        Oel_Volumenstrom = client.get_node("ns=5;s=Root//Control Network//TLP//Applications//Mönch//Control Modules//Mönch//Schmierölsystem//M_D44:SO.Out")
        Oel_Temperatur_Tank = client.get_node("ns=5;s=Root//Control Network//TLP//Applications//Mönch//Control Modules//Mönch//Schmierölsystem//M_D50:IO.In.Value")
        Oel_Temperatur_nach_Mischventil = client.get_node("ns=5;s=Root//Control Network//TLP//Applications//Mönch//Control Modules//Mönch//Schmierölsystem//M_D40:IO.In.Value")
        #Oel_Temperatur_Turbine_Eingang = client.get_node("...")
        Mischventil_IST_Stellwert = client.get_node("ns=5;s=Root//Control Network//TLP//Applications//Mönch//Control Modules//Mönch//Schmierölsystem//M_D5:IO.Out.Value")
        
        Testvariabel_zum_auf_LS_schreiben = client.get_node("ns=5;s=Root//Control Network//TLP//Applications//Mönch//Control Modules//Mönch//Schmierölsystem:TestVar_OPC_Rasp")

        Input_nodes = {Oel_Volumenstrom,Oel_Temperatur_Tank,Oel_Temperatur_nach_Mischventil,Mischventil_IST_Stellwert}
        Output_nodes = {Testvariabel_zum_auf_LS_schreiben}
        i=345
        while True:
            time.sleep(0.2)
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
