import time
import os
import sys
from plots import meinePlots

# Füge den Pfad zum übergeordneten Verzeichnis zum sys.path hinzu
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)

from OPC.opcua_client_monitor import OpcUaClient

if __name__ == "__main__":
    p = meinePlots()
    c = OpcUaClient(0.1,p)

    try:
        while True:
            time.sleep(0.1)
            if not c.is_running():
                raise 
    
    except Exception as e:
        print(e)
    except KeyboardInterrupt:
        print("Keyboard interrupt received. Exiting...")
    finally:
        c.loop_stop()
        p.loop_stop()