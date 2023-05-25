from opcua import Client

# Verbindung zum OPC-UA-Server herstellen
url = "opc.tcp://192.168.43.97:4840/freeopcua/server/" #lenovo hotspot
#url = "opc.tcp://192.168.43.203:4840/freeopcua/server/" #raspi hotspot
client = Client(url)

# Verbindung herstellen und Verbindungsstatus überprüfen
try:
    client.connect()
    print("Verbindung hergestellt")
    # Verbindung trennen
    client.disconnect()
except Exception as e:
    print("Fehler beim Verbindungsaufbau:", e)

# Weitere Operationen mit dem OPC-UA-Server durchführen...

