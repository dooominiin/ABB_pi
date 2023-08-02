import sys
from OPC.opcua_client import OpcUaClient
from OPC.opcua_monitoring_server import OpcUaServer_Monitoring
from Regler.Regler_loop import Regler
import time
import os


# Ermittle den Pfad zum Verzeichnis des Skripts
script_dir = os.path.dirname(os.path.abspath(__file__))
# Setze das Arbeitsverzeichnis auf das Verzeichnis des Skripts
os.chdir(script_dir)

# Öffne eine Logdatei zum Schreiben
log_datei = open('main.log', 'a')

# Umlenken der Standardausgabe (stdout) auf die Logdatei
sys.stdout = log_datei

# Umlenken der Standardfehlerausgabe (stderr) auf die Logdatei
sys.stderr = log_datei

print("main.py gestartet")



server = OpcUaServer_Monitoring()
r = Regler(dt = 0.1, server=server)

c = OpcUaClient(dt = 0.01,regler = r)

c.loop_start()
r.loop_start()

try:
    while c.is_running() or r.is_running() or server.is_running():
        time.sleep(0.1)

except KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
finally:
    r.loop_stop()
    c.loop_stop()
    server.loop_stop()
    log_datei.close()
