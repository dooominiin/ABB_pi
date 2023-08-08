import time
import os
import sys

# Füge den Pfad zum übergeordneten Verzeichnis zum sys.path hinzu
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)

from OPC.opcua_client_monitor import OpcUaClient

if __name__ == "__main__":
    c = OpcUaClient(0.1)
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        c.loop_stop()