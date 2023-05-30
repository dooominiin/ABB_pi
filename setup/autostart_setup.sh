#!/bin/bash
# fügt einen autostarteintrag für den Regler hinzu

# Überprüfe, ob die Zeile bereits vorhanden ist
if ! grep -q "@lxterminal -e python3 /home/mister/Desktop/ABB_Projekt/main.py" /etc/xdg/lxsession/LXDE-pi/autostart; then
  # Füge die Zeile am Ende der Datei hinzu
  echo "@lxterminal -e python3 /home/mister/Desktop/ABB_Projekt/main.py" | sudo tee -a /etc/xdg/lxsession/LXDE-pi/autostart > /dev/null
  echo "Die Autostart Zeile wurde erfolgreich hinzugefügt."
  
  # Führe einen Neustart des Raspberry Pi aus
  sudo reboot
else
  echo "Die Autostart Zeile ist bereits in der Datei vorhanden."
fi


