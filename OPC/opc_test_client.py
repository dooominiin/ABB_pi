from threading import Thread
import time
import logging
from opcua import Client
import OpenOPC

# Konfiguration des Logging
log_file = 'log_file.txt'
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


c = OpenOPC.client("opc.tcp.172.16.4.150.48050")
print(c.servers())

#test