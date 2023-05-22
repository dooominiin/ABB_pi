#!/bin/bash

while true
do
    # Starten des Python-Skripts
    /usr/bin/python3 /home/mister/Desktop/ABB_Projekt/OPC/opc_test_server.py

    # Überprüfen, ob das Skript noch läuft
    if [ $? -eq 0 ]; then
        echo "Skript wird ausgeführt."
    else
        echo "Skript wurde beendet. Starte neu..."
    fi

    # Warten für eine gewisse Zeit, bevor das Skript erneut gestartet wird
    sleep 10
done
