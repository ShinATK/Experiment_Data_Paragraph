import numpy as np
import math
from scipy import integrate
import matplotlib.pyplot as plt

def Gaussion(E, E0):

    Nt = 1e27   # 总的态密度
    q = 0.05    # 高斯分布宽度

    G = Nt*math.exp(-(E-E0)**2/(2*q**2))/(q*(2*math.pi)**(0.5))

    return G

def Femi_Dirac(E, kT=0.0258):

    F_D = (1 + math.exp((E-Ef)/kT))

    return F_D

def N(V, Ef):

    E0 = -5  # 高斯分布中心能级
    N = integrate(Gaussion(E+V, E0)*Femi_Dirac(E), -float("inf"),float("inf"))

    return N