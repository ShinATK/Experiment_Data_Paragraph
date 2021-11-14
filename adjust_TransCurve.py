import numpy as np
import matplotlib.pyplot as plt

ds = [3, 6, 9, 12]
VT = [4.1,8.1,12.2,16.2]

a = np.linspace(-2, 0, len(np.loadtxt(f"阈值电压为0的转移曲线电流.txt")))
np.savetxt("a", a, fmt="%0.8f")


