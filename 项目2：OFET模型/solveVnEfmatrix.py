import numpy as np
import math
from scipy import integrate
import matplotlib.pyplot as plt

nd = 1000                       # 分割份数
V0 = 0                          #
Vg = 0                          # 栅压初始值
dv = -0.1                       # 电压步长
Vg_max = -120                   # 最大栅压
ds = 10e-9                      # 薄膜厚度 10nm
n = int((Vg_max - Vg)/dv + 1)
V_matrix = np.zeros(nd+1, n)    # 初始化电压矩阵
n_matrix = np.zeros(nd+1, n)    # 初始化电荷密度矩阵



for i in range(1, n+1, 1):
    print(f'{Vg} \n {n} \n')

    if Vg > 0:
        print('栅压大于零')
        break

    elif Vg <= 0:
        print()

