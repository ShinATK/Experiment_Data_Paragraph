import numpy as np
import matplotlib.pyplot as plt

A = 1
B = 1/2
Vd = -20

Isd_results = {}
Isd = []

Vg = np.arange(-40, 20, 0.1)
# Vt = np.arange(0, 5, 1)
Vt = [4.1, 8.1, 12.2, 16.2]

def Vg_range(Vt):
    return np.arange(-40, Vt, 0.1)

def linear_curve(Vg, Vt):
    Isd=A*((Vg-Vt)*Vd - 0.5*Vd**2)
    return Isd

def saturation_curve(Vg, Vt):
    Isd = B*(Vg-Vt)**2
    return Isd


for each_Vt in Vt:
    for each_Vg in Vg:
        if each_Vg > each_Vt:
            break
        else:
            if each_Vg < (each_Vt + Vd):
                Isd.append(linear_curve(each_Vg, each_Vt))
            else:
                Isd.append(saturation_curve(each_Vg, each_Vt))


    Isd_results[each_Vt] = Isd
    Isd = []

plt.subplot()
plt.xlabel('Vg(V)', fontsize=14)
plt.ylabel('Isd(A)', fontsize=14)
plt.axes(yscale='log')

for each_Vt in Vt:
    plt.plot(Vg_range(each_Vt), Isd_results[each_Vt], label=f"Threshold {each_Vt}V")
plt.legend()
plt.show()