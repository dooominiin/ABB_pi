import subprocess
import os
import sys
import signal
import datetime 

#Dieses Script wird periodisch mit chrontab ausgeführt. 
#Es prüft, ob der Regler/OPC-Client (main.py) läuft. 
#Wenn nicht, wird das programm neu gestartet.

# Ermittle den Pfad zum Verzeichnis des Skripts
script_dir = os.path.dirname(os.path.abspath(__file__))
# Setze das Arbeitsverzeichnis auf das Verzeichnis des Skripts
os.chdir(script_dir)

log_datei = open('check_and_start.log', 'a')
    # Umlenken der Standardausgabe (stdout) auf die Logdatei
sys.stdout = log_datei
    # Umlenken der Standardfehlerausgabe (stderr) auf die Logdatei
sys.stderr = log_datei



def is_process_running(process_name):
    try:
        ps_output = subprocess.check_output(["pgrep", "-f", process_name])
        #print("Prozess {} gefunden! ".format(process_name))
        return True
    except subprocess.CalledProcessError:
        print("Prozess {} nicht gefunden! ".format(process_name))
        return False

def start_process(process_name):
    if not is_process_running(process_name):
        print("Der Prozess {} wird neu gestartet!\t{}".format(process_name,datetime.datetime.now().time()))
        subprocess.Popen(["python3", "/home/mister/Desktop/ABB_Projekt/main.py"])

def stop_process(process_name):
    if is_process_running(process_name):
        try:
            pid = int(subprocess.check_output(["pgrep", "-f", process_name]))
            os.kill(pid, signal.SIGTERM)
            print("Der Prozess {} (PID {}) wurde beendet.\t{}".format(process_name, pid,datetime.datetime.now().time()))
        except subprocess.CalledProcessError:
            print("Der Prozess {} wurde nicht gefunden.".format(process_name))
        except OSError as e:
            print("Fehler beim Beenden des Prozesses {}: {}".format(process_name, e))

if __name__ == "__main__":
    # Stopt oder startet zyklisch das main.py und damit den kompletten regler/OPC 
    
    process_name = "/home/mister/Desktop/ABB_Projekt/main.py"
    #stop_process(process_name)
    start_process(process_name)
