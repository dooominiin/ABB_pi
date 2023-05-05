from OPC.opcua_client import OpcUaClient
from Regler.Regler_loop import Regler
import time

r = Regler(dt = 1)
c = OpcUaClient(dt = 0.01)
c.set_regler_client_reference(r)

c.loop_start()
r.loop_start()

try:
    while True:
        time.sleep(0.1)
except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
finally:
    r.loop_stop()
    c.loop_stop()
