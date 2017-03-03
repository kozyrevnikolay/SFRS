import numpy as np


def Brillouin(x, S):
    a1 = (2*S+1)/(2*S)
    a2 = 1/(2*S)
    if np.any(x):
        y = a1/np.tanh(a1*x) - a2/np.tanh(a2*x)
    else:
        y = 0
    return y
