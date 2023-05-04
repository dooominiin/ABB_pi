from scipy import signal
import numpy as np
import matplotlib.pyplot as plt

def multiply_lti_systems(sys1, sys2):
    # Get the numerator and denominator of both systems
    num1, den1 = sys1.num, sys1.den
    num2, den2 = sys2.num, sys2.den
    
    # Multiply the numerators and denominators element-wise
    num_product = np.polymul(num1, num2)
    den_product = np.polymul(den1, den2)
    
    # Create the resulting system
    sys_product = signal.lti(num_product, den_product)
    
    return sys_product

ki = 100
kp = 10

# Define the continuous-time system
A = np.array([0.])
B = np.array([1.])
C = np.array([ki])
D = np.array([kp])

# Define the sampling time
Ts = 0.1

# Compute the discrete-time transfer function using the Tustin method
C_cont = signal.lti(A,B,C,D)
C_disc = signal.cont2discrete((A,B,C,D), Ts, method='bilinear')

P_cont = signal.lti((1.),(1.,10.))
P_disc = signal.cont2discrete(((1.),(1.,10.)), Ts, method='bilinear')

print(C_disc)

PC = C_cont.__mul__(C_cont)
t, x = PC.step(T=np.linspace(0, 50, 100))

fig, ax = plt.subplots()

ax.plot(t, x, label='Continuous', linewidth=3)



