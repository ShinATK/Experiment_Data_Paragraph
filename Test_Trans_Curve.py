import numpy as np
import matplotlib.pyplot as plt

W = 3e-3 # 3mm
L = 3e-4 # 300μm
C = 11.9e-5
miu = 0.1e-4 # 0.1cm2V-1s-1

A = W*C*miu/L
B = A/2
Vd = -20

Isd_results = {}
Isd = []

ds = [None, 3, 6, 9, 12]
Vg = np.arange(-60, 20, 0.1)
delta_Vg = 80
# Vt = np.arange(0, 5, 1)
Vt = [0, -60+delta_Vg*0.5, -60+delta_Vg*0.65, -60+delta_Vg*0.8, -60+delta_Vg*0.95]

def Vg_range(Vt):
    return np.arange(-60, Vt, 0.1)

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
    np.savetxt(f"阈值电压为{each_Vt}的转移曲线电流.txt", Isd, fmt="%0.12f")
    Isd = []

plt.subplot()
plt.axes(yscale='log')
plt.xlabel('Vg(V)', fontsize=14)
plt.ylabel('Isd(A)', fontsize=14)

for each_Vt in Vt:
    plt.plot(Vg_range(each_Vt), Isd_results[each_Vt],
             label=f"{ds[Vt.index(each_Vt)]}nm Threshold Voltage {each_Vt}V")

plt.legend()
plt.show()