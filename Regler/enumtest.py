from enum import Enum

class Zustand(Enum):
    manueller_Betrieb = 0
    geregelter_Betrieb = 1

print(Zustand.geregelter_Betrieb==Zustand(1))