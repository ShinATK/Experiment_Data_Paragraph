import numpy as np
import matplotlib.pyplot as plt


def cal_interp_x0(polynomial, x0):
    """
    计算所给定的插值点的数值，即插值
    :param polynomial：插值多项式
    :param x0：所求插值的x坐标
    """
    x0 = np.asarray(x0, dtype=float)
    n0 = len(x0)  # 所求插值点的个数
    y_0 = np.zeros(n0)  # 存储插值点x0对应的插值
    t = polynomial.free_symbols.pop()  # 返回值为集合，获取插值多项式的自由变量
    # print(t)

    for i in range(n0):
        y_0[i] = polynomial.evalf(subs={t: x0[i]})

    return y_0


def plt_interpolation(params):
    """
    可视化插值图像与所求的插值点
    """
    polynomial, x, y, title, x0, y0 = params
    plt.figure(figsize=(8, 6))
    plt.plot(x, y, "ro", label="Interpolation base points")

    xi = np.linspace(min(x), max(x), 100)  # 模拟100个值
    yi = cal_interp_x0(polynomial=polynomial, x0=xi)
    plt.plot(xi, yi, "b--", label="Interpolation polynomial")

    if x0 is not None and y0 is not None:
        plt.plot(x0, y0, "g*", label="Interpolation point values")

    plt.legend()
    plt.xlabel("Vt", fontdict={"fontsize": 12})
    plt.ylabel("Prints num", fontdict={"fontsize": 12})
    plt.title(title+"interpolation polynomial and values", fontdict={"fontsize": 14})
    plt.grid(ls=":")
    plt.show()