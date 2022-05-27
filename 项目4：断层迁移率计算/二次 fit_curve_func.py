from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt
import os
import csv

path_set = 'Data/'
def load_files(path=path_set):
    # 读取 path 下的所有文件的文件名
    files_name = os.listdir(path)

    # 存储后缀名为csv的文件名称
    files_csv = []

    # 根据后缀名筛选出csv文件
    for each in files_name:
        files_extension = os.path.splitext(each)[1]
        # print(files_extension)
        if files_extension == '.csv':
            files_csv.append(each)
    # 按文件名排序
    files_csv.sort()
    return files_csv

def load_csv_data(filename, path=path_set):
    load_file_csv = open(path + filename) # 打开csv文件
    read_file_csv = csv.reader(load_file_csv) # 读取csv文件
    data = list(read_file_csv)
    x_Voltage = list()
    y_Current = list()

    for i in range(1, len(data)):
        x_Voltage.append(float(data[i][6]))  # 栅极电压在第6列
        y_Current.append(abs(float(data[i][4])))  # 源极电流在第4列

    return np.array(x_Voltage), np.array(y_Current), data

e = 1.6e-19
L = 3e-4  # 300μm
W = 3e-3  # 3mm
d = 1e-8  # 10nm
C = 11.9e-9  # F

def fit_func(Vg, m, Vt):
    Isd=W*C*m*(Vg-Vt)**2/(2*L)
    return Isd

csv_name = load_files()
csv_name.sort()
for each_name in csv_name:
    paramV, paramI, data = load_csv_data(each_name)
    Vg = paramV[:51]
    Isd = paramI[:51]

    popt, pcov = curve_fit(fit_func, Vg, Isd, maxfev=100000)
    m,Vt = popt[0:2]
    spvals=fit_func(Vg, m,Vt)
    plt.plot(Vg, Isd, '*')
    plt.plot(Vg, spvals, 'r')
    plt.title(each_name[:-4]+' a=%f, b=%f'%(m,Vt))
    plt.show()

