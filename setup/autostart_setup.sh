#!/bin/bash
# Fügt einen Autostart-Eintrag für den Regler hinzu

# Pfad zur Log-Datei
LOG_FILE="/home/mister/Desktop/ABB_Projekt/main.log"

# Überprüfe, ob die Zeile bereits vorhanden ist
if ! grep -q "@lxterminal -e python3 /home/mister/Desktop/ABB_Projekt/main.py >> \"$LOG_FILE\" 2>&1" /etc/xdg/lxsession/LXDE-pi/autostart; then
  # Füge die Zeile am Ende der Datei hinzu
  echo "@lxterminal -e python3 /home/mister/Desktop/ABB_Projekt/main.py >> \"$LOG_FILE\" 2>&1" | sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null
  echo "Die Autostart-Zeile wurde erfolgreich hinzugefügt."
else
  echo "Die Autostart-Zeile ist bereits in der Datei vorhanden."
fi
