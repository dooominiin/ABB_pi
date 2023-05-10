import numpy as np

class rohrstück_diskret:
    def __init__(self, A, B, C, D, startwert):
        self.A = A
        self.B = B
        self.C = C
        self.D = D
        self.x = np.ones(A.ndim)*startwert
        self.x_neu = np.ones(A.ndim)*startwert
        self.u = 0
        self.y = 0
    
    def update(self, u, F):
                
        # Berechne neuen Zustand
        self.x_neu = self.A @ self.x + self.B @ u
        
        # Berechne Ausgang
        self.y = self.C @ self.x + self.D @ u
        
        # Speichere den neuen Zustand
        self.x = self.x_neu
        
        return self.y
