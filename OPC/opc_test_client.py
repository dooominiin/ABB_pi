from threading import Thread
import time
from opcua import Server
#fdsgbfdgf
class OpcUaServer:
    def __init__(self, dt, regler):
        self.server = Server()
        self.server.set_endpoint("opc.tcp://localhost:4840/freeopcua/server/")
        #self.server.allow_remote_administration(True)
        
        self.regler = regler
        self.regler.set_opc_server(self.server)
        
        self.dt = dt  # Diskretisierungszeitschritt
        self.terminate = False
        self.thread = Thread(target=self.loop_forever)
        self.output_node = None

    def create_variables(self):
        root = self.server.get_root_node()
        objects_node = self.server.get_objects_node()

        # Erstellen der Variablen
        temperaturen_node = objects_node.add_object(2, "Temperaturen")
        
        variable_names = ["T_D40", "T_tank", "T_t", "F", "s", "r"]
        for var_name in variable_names:
            variable_node = temperaturen_node.add_variable(2, var_name, 0.0)
            variable_node.set_writable(True)
        
        # Einen Ausgabeknoten erstellen
        self.output_node = temperaturen_node.add_variable(2, "Output", 0.0)
        self.output_node.set_writable(True)

    def start_server(self):
        self.server.start()
        self.create_variables()
        print("OPC-UA-Server gestartet.")

    def stop_server(self):
        self.terminate = True
        self.thread.join()
        self.server.stop()
        print("OPC-UA-Server gestoppt.")

    def loop_forever(self):
        while not self.terminate:
            start_time = time.time()  # Startzeit speichern
            elapsed_time = time.time() - start_time  # Zeit seit Start speichern
            time.sleep(max(0, self.dt - elapsed_time))  # Schlafzeit berechnen und warten
            # Hier kannst du deine Logik für die Aktualisierung der Variablen einfügen
            # Beispiel: self.output_node.set_value(self.regler.get_output())

    def start(self):
        self.thread.start()

    def stop(self):
        self.terminate = True
        self.thread.join()

        
if __name__ == "__main__":
    from threading import Thread
    import time

    class Regler:
        def set_opc_server(server):
            server = server

        def get_output():
            # Hier kannst du deine eigene Logik für die Ausgabe des Reglers einfügen
            return 0


    s = OpcUaServer(dt=1, regler = Regler)
    s.start_server()