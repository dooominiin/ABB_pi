#!/usr/bin/python3

import sys
from OPC.opcua_client import OpcUaClient
from OPC.opcua_monitoring_server import OpcUaServer_Monitoring
from Regler.Regler_loop import Regler
import time
import os
import datetime

loggen = True
if loggen:
    
    # Öffne eine Logdatei zum Schreiben
    log_datei = open('main.log', 'a')
    # Umlenken der Standardausgabe (stdout) auf die Logdatei
    sys.stdout = log_datei
    # Umlenken der Standardfehlerausgabe (stderr) auf die Logdatei
    sys.stderr = log_datei


# Ermittle den Pfad zum Verzeichnis des Skripts
script_dir = os.path.dirname(os.path.abspath(__file__))
# Setze das Arbeitsverzeichnis auf das Verzeichnis des Skripts
os.chdir(script_dir)

print("main.py gestartet")


# OPC-Server zum überwachen des Reglers, enthält alle States des Reglers
server = OpcUaServer_Monitoring(aktualisierungsintervall = 1)

# Smithpredictor Regler Objekt, dt = Diskretisierungszeitschritt [s]
regler = Regler(dt = 0.1, server=server)

# OPC-Client, verbunden mit Leitsystem, INPUT + OUTPUT
client = OpcUaClient(dt = 0.01,regler = regler, output_update_intervall = 1)

client.loop_start()
regler.loop_start()

try:
    while client.is_running() or regler.is_running() or server.is_running():
        if (not client.is_running()) or (not regler.is_running()) or (not server.is_running()):
            print("Client: {}\tServer: {}\tRegler: {}".format(client.is_running(), regler.is_running(), server.is_running()))
            try: 
                regler.loop_stop()
                client.loop_stop()
                server.loop_stop()
            except Exception as e:
                print(e)
            print("Client: {}\tServer: {}\tRegler: {}".format(client.is_running(), regler.is_running(), server.is_running()))
        time.sleep(0.1)

except :#KeyboardInterrupt:
    print("Keyboard interrupt received. Exiting...")
finally:
    regler.loop_stop()
    client.loop_stop()
    server.loop_stop()
    print("gestopt :{}".format(datetime.datetime.now().time()))
    if loggen: log_datei.close()
