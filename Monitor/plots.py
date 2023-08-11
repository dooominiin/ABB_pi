import time
from threading import Thread
import os, sys
import numpy as np
import h5py

# Füge den Pfad zum übergeordneten Verzeichnis zum sys.path hinzu
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_directory)
from Regler.Smithpredictor import Smithpredictor

class meinePlots(): 
    def __init__(self):
        self.neue_Daten = False
        self.delay = 0.2
        self.terminate = False
        self.thread = Thread(target=self.loop_forever)
        self.data_neu = Smithpredictor.states_dictionary()
        self.data_neu['time'] = 0
        self.data = Smithpredictor.states_dictionary_array()
        self.data['time'] = np.array(0)
        self.start_time = time.time()
        self.loop_start()
        
    def set_new_Data(self,node,value):
        name = str(node)[21:]
        self.set_neue_Daten_flag()
        self.data_neu[name] = value
    

    def set_neue_Daten_flag(self):
        self.neue_Daten = True

    def loop_forever(self):
        while not self.terminate:
            time.sleep(0.01)
            if self.neue_Daten:
                # warte eine kurze zeit damit alle variabeln aktualisiert wurden
                time.sleep(self.delay)
                
                # Datenset erweitern
                self.data_neu['time'] = time.time()-self.start_time
                for key, new_value in zip(self.data.keys(), self.data_neu.values()):
                    self.data[key] = np.append(self.data[key],new_value)
                self.neue_Daten = False
                # Datenset lokal speichern für das Matlab programm zum plotten
                try:
                    t1 = time.time()
                    # Dateinamen festlegen
                    filename = 'data.h5'

                    with h5py.File(filename, 'w') as f:
                        try:
                            group = f.create_group("States")
                        except Exception as e:
                            print("fehler: {}".format(e))
                        for key, value in self.data.items():
                            try:
                                group.create_dataset(key,data=value)
                            except Exception as e:
                                raise
                                print("fehler bei create_dataset:  {}".format(e))
                except Exception as e:
                    print(e)
                    raise
                finally:
                    t2 = time.time()
                    print("Benötigte Zeit zum Speichern des Datensets mit der Grösse {} : {:.4f}s".format(len(self.data['F']),t2-t1))



















    def loop_start(self):
        if not self.terminate:
            self.thread.start()
            print("plot Thread gestartet!")

    def loop_stop(self):
        self.terminate = True
        try:
            self.thread.join()
        except Exception as e:
            print(e)
                
        