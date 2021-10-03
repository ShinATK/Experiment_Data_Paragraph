from lagrange_interpolation import LagrangeInterpolation
import numpy as np


if __name__ == "__main__":

    n = 1e-5
    # 打印次数为X，阈值电压为Y
    y = np.loadtxt('Vg(-40 4).txt')
    x = np.arange(-40, 5, 0.5)
    x0 = np.array([7, 8, 9])


    lag_interp = LagrangeInterpolation(x, y)
    lag_interp.fit_interp()


    y0 = lag_interp.cal_interp_x0(x0)
    print("所求插值点的值：", y0)
    lag_interp.plt_interpolation(x0, y0)

