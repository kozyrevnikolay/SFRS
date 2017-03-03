import math as m
import numpy as np
import universal_constants as uc
import Brillouin as B
import glb


def without_selection_rules(t, n):
    omega_L = glb.g_Mn*uc.mu*np.sqrt(glb.B_exch**2+glb.B_ext**2)/uc.h
    delta = np.arctan(glb.B_exch/glb.B_ext)
    N = glb.N_Mn*glb.S*np.sin(delta)*(1-np.cos(omega_L*t))
    output = np.exp(-t/glb.tau)*N**n*np.exp(-N)/(glb.tau*m.factorial(n))
    return output


def with_selection_rules(t, phi, n):
    # Angular function of distribution.
    G = np.array(np.exp(-(phi-glb.phi0)**2/(2*glb.sigma**2))/(np.sqrt(2*m.pi)*glb.sigma))
    # Heavy Hole energy splitting.
    amplitude1 = glb.bettaN0*glb.x*glb.S
    argument1 = uc.mu*glb.g_Mn*glb.S*glb.B_ext*np.sin(phi)/(uc.k*glb.T)
    deltaE = amplitude1*B.Brillouin(argument1, glb.S)
    # N(t) - number of precessing Mn ions.
    argument2 = uc.mu*glb.g_Mn*glb.S*glb.B_ext/(uc.k*glb.T)
    avgS = glb.S*B.Brillouin(argument2, glb.S)
    B_tot = np.sqrt(glb.B_ext**2 + glb.B_exch**2 + 2*glb.B_exch*glb.B_ext*np.sin(phi))
    omega_L = uc.mu*glb.g_Mn*B_tot/uc.h
    delta = np.arctan((glb.B_exch + glb.B_ext*np.sin(phi))/(glb.B_ext*np.cos(phi)))
    N = glb.N_Mn*avgS*np.sin(delta)**2*(1-np.cos(omega_L*t))
    # Main output of the function.
    output = G*0.5*(1+((-1)**n)*np.cos(deltaE*t/uc.h))*np.exp(-N)*np.exp(-t/glb.tau)*N**n/(glb.tau*m.factorial(n))
    return output
