import time
import subprocess

while True:
    try:
        subprocess.run(['scp', 'raspi@10.84.2.204:~/Desktop/Zeitraffer/mylist.txt', 'C:/Users/domin/OneDrive - FHNW/ABB_Regler/Raspberry pi git/ABB_pi'], check=True)
        print("Datei erfolgreich kopiert!")
    except subprocess.CalledProcessError as e:
        print("Fehler beim Kopieren der Datei:", e)

    time.sleep(5)
