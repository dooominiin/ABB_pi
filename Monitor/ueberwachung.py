class Monitor:
    # Diese Klasse aktualisiert die States des Reglers in einem Server, damit extern die zustände des Reglers überwacht werden können. 
    def __init__(self, server):
        self.timer = 0
        self.zeitintervall = server.get_intervall()
        self.server = server
    
    def step(self, dt):
        self.timer += dt
        flag = False
        if self.timer >= self.zeitintervall:
            self.timer = 0
            flag = True
        return flag

    def update(self, states):
        self.server.update(states)
        
    # Alle Zustände im Smithpredictor
    def states_dictionary():
        d = {
            's' : 0,
            'F' : 0,
            'F1': 0,
            'F2': 0,
            'F3': 0,
            'T_D40': 0,
            'TOELE': 0,
            'T_T_1': 0,
            'T_T_2': 0,
            'f': 0,
            's_k': 0,
            's_k2': 0,
            'k' : 0,
            's_V': 0,
            's_V_K': 0,
            'r_tilde': 0,
            'T_BP1': 0,
            'T_BP2': 0,
            'T_WT1': 0,
            'T_WT2': 0,
            'T_V_tilde': 0,
            'T_V': 0,
            'T_V2': 0,
            'm': 0,
            'r_alt': 0,
            'r': 0,
            'T_tank': 0,
            'T_kuehl': 0,
            'güte_M': 0,
            'güte_K' : 0,
            'güte_r' : 0
            # Füge hier weitere Schlüssel hinzu, falls benötigt
        }
        return d
