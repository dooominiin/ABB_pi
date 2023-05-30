import sys
from OPC.opcua_client import OpcUaClient
from Regler.Regler_loop import Regler
import time

# Öffne eine Logdatei zum Schreiben
log_datei = open('main.log', 'w')

# Umlenken der Standardausgabe (stdout) auf die Logdatei
sys.stdout = log_datei

# Umlenken der Standardfehlerausgabe (stderr) auf die Logdatei
sys.stderr = log_datei

print("main.py gestartet")




r = Regler(dt = 0.1)

c = OpcUaClient(dt = 0.01,regler = r)

c.loop_start()
r.loop_start()

try:
    while c.is_running() or r.is_running():
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
finally:
    r.loop_stop()
    c.loop_stop()
    log_datei.close()