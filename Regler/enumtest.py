from enum import Enum
import json

class Zustand(Enum):
    manueller_Betrieb = 0
    geregelter_Betrieb = 1

class aba:
        def __init__(self):
        
        # JSON laden und Namen auslesen
            with open("OPC/variablen.json", "r", encoding='utf-8') as file:
                variables = json.load(file)
                variable_names = [var_info["name"] for var_info in variables]
                # Input-Liste initialisieren
                self.input = {name: 60 if name.startswith("T") else 0 for name in variable_names}

            print(self.input)
            print(Zustand.manueller_Betrieb==Zustand(self.input["state"]))

a = aba()
