import os

class LogFile:
    def __init__(self, dateiname, variabelnamen ,anzahl_zeilen, Zeitschritt):
        # Zeitschritt bestimmt, in welchem intervall datenpunkte gespeichert werden
        self.dateiname = dateiname
        self.anzahl_zeilen = anzahl_zeilen
        self.zeilen_index = 1
        self.time_index = 0
        self.zähler = 0
        self.Zeitschritt = Zeitschritt
        with open(self.dateiname, 'w') as datei:
            datei.write(f"{variabelnamen}, reihenfolge\n")  # Zeile 1 mit dem String 'names' initialisieren
            for _ in range(self.anzahl_zeilen):
                datei.write('\n')  # Leere Zeilen hinzufügen

    def update(self, text, dt):
        if self.Zeitschritt <= self.zähler:
            self.zähler = 0
            with open(self.dateiname, 'r+') as datei:
                datei.seek(0, os.SEEK_SET)  # Den Dateizeiger ans Anfang der Datei setzen
                zeilen = datei.readlines()
                if self.zeilen_index < len(zeilen):
                    zeilen[self.zeilen_index] = f"{text},{self.time_index:12.2f}\n"
                    datei.seek(0, os.SEEK_SET)  # Den Dateizeiger erneut ans Anfang der Datei setzen
                    datei.writelines(zeilen)
                else:
                    print(f"Der Zeilenindex {self.zeilen_index} ist außerhalb des gültigen Bereichs.")
            self.zeilen_index = self.zeilen_index%(self.anzahl_zeilen)
            self.zeilen_index += 1
        self.time_index += dt
        self.zähler += dt

if __name__ == "__main__":
    # Beispielaufruf
    dateiname = 'test.txt'
    anzahl_zeilen = 10

    log = LogFile(dateiname, "michi,hans,peter",anzahl_zeilen)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
    log.update('Dies ist die neue Zeile.', 0.1)
