#!/bin/bash
# entfernt den autostarteintrag für den Regler

# Überprüfe, ob die Zeile vorhanden ist
if grep -q "@lxterminal -e python3 /home/mister/Desktop/ABB_Projekt/main.py" /etc/xdg/lxsession/LXDE-pi/autostart; then
  # Entferne die Zeile aus der Datei
  sudo sed -i '/@lxterminal -e python3 \/home\/mister\/Desktop\/ABB_pi\/main.py/d' /etc/xdg/lxsession/LXDE-pi/autostart
  echo "Der Autostart-Eintrag wurde erfolgreich entfernt."

  # Führe einen Neustart des Raspberry Pi aus
  sudo reboot
else
  echo "Der Autostart-Eintrag ist nicht in der Datei vorhanden."
fi
