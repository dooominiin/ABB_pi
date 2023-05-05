import threading
import time
import signal
from Regler.Reglermodell import Smithpredictor  # Importiere die Regler-Klasse aus Reglermodell


# Hier werden die Threads für den OPC client sowie den Regler gestartet. 
# Timestep variables
Ts_OPC = 0.01
Ts_Regler = 0.3

# Shared variables
Input = 1
Output = 2
lock = threading.Lock()
stop_threads = False

def thread_1_OPC_client():
    global Input, Output, stop_threads
    while not stop_threads:
        start_time = time.time()  # Startzeit speichern
        with lock:
            Input = Output
        print("Ausführungszeit thread_1_OPC_client: {:.3f} ms".format((time.time() - start_time)*1000))
        elapsed_time = time.time() - start_time  # Zeit seit Start speichern
        time.sleep(max(0, Ts_OPC - elapsed_time))  # Schlafzeit berechnen und warten
        with lock:
            Input = Output  # Aktualisiere Input mit dem letzten Output

def thread_2_Regler_update():
    global Input, Output, stop_threads
    regler = Smithpredictor(Ts_Regler)  # Initialisiere den Regler
    while not stop_threads:
        start_time = time.time()  # Startzeit speichern
        with lock:
            Output = regler.update(Input)  # Verwende die Regler-Klasse, um Output zu berechnen
        print("Ausführungszeit thread_2_Regler_update: {:.3f} ms".format((time.time() - start_time)*1000))
        elapsed_time = time.time() - start_time  # Zeit seit Start speichern
        time.sleep(max(0, Ts_Regler - elapsed_time))  # Schlafzeit berechnen und warten

# Create threads
t1 = threading.Thread(target=thread_1_OPC_client)
t2 = threading.Thread(target=thread_2_Regler_update)

# Start threads
t1.start()
t2.start()

# Wait for keyboard interrupt
def signal_handler(signal, frame):
    global stop_threads
    print("\nProgram terminated by user.")
    stop_threads = True

signal.signal(signal.SIGINT, signal_handler)

# Wait for threads to stop
while t1.is_alive() or t2.is_alive():
    time.sleep(0.1)

print("Threads stopped.")
