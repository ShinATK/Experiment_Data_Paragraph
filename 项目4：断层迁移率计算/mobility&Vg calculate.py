import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import math


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

# 定义计算离散点导数的函数
def cal_deriv(x, y):  # x, y的类型均为列表
    diff_x = []  # 用来存储x列表中的两数之差
    for i, j in zip(x[0::], x[1::]):
        diff_x.append(j - i)

    diff_y = []  # 用来存储y列表中的两数之差
    for i, j in zip(y[0::], y[1::]):
        diff_y.append(j - i)

    slopes = []  # 用来存储斜率
    for i in range(len(diff_y)):
        slopes.append(diff_y[i] / diff_x[i])

    deriv = []  # 用来存储一阶导数
    for i, j in zip(slopes[0::], slopes[1::]):
        deriv.append(((i + j) / 2))  # 根据离散点导数的定义，计算并存储结果
    deriv.insert(0, slopes[0])  # (左)端点的导数即为与其最近点的斜率
    deriv.append(slopes[-1])  # (右)端点的导数即为与其最近点的斜率

    #for i in deriv:  # 打印结果，方便检查，调用时也可注释掉
    #     print(i)

    return deriv  # 返回存储一阶导数结果的列表

def text_save(filename, data):  # filename为写入CSV文件的路径，data为要写入数据列表.
    file = open(f'./data/{filename}', 'a')
    for i in range(len(data)):
        s = str(data[i]).replace('[', '').replace(']', '')  # 去除[],这两行按数据不同，可以选择
        s = s.replace('{', '').replace('}', '')
        s = s.replace("'", '').replace(',', '') + '\n'  # 去除单引号，逗号，每行末尾追加换行符
        file.write(s)
    # file.write(data+'\n')
    file.close()
    print(filename+"保存文件成功")

if __name__ == '__main__':

    csv_name = load_files()
    csv_name.sort()
    filename = '20220511 PCDTPT Point 01'

    e=1.6e-19
    L=3e-4 # 300μm
    W=3e-3 # 3mm
    C=11.9e-9 # F
    Vsd=-5 # V

    start_point = 0
    end_point = 60

    i = 0
    count = len(csv_name)

    for each_name in csv_name:

        i += 1
        print(f'({i}/{count})Running {filename} {each_name}...')

        paramV, paramI, data = load_csv_data(each_name)

        # plt.plot(paramV[35:45], paramI[35:45], label=each_name[:-4])
        fig1, ax = plt.subplots(1, 1)
        ax.semilogy()
        plt.plot(paramV[start_point:end_point], paramI[start_point:end_point], label=each_name[:-4])
        font = {'family': 'Times New Roman',
                 'weight': 'normal',
                 'style': 'italic',
                 'size': 14
                 }
        plt.xlabel('V$_g$ (V)', font)
        plt.ylabel('-I$_s$$_d$ (A)', font)
        plt.legend()
        plt.title(f'Trans Curve {each_name[:-4]}')
        plt.tight_layout()
        plt.savefig('./Data/' + f'线性区 Trans_Curve {filename} ' + each_name[:-4] + '.png', dpi=720)
        # plt.show()
        plt.close()


        k = cal_deriv(paramV[start_point:end_point], paramI[start_point:end_point])
        # A = L / (W * C * Vsd)
        A = 1.7e6

        mobility = abs(A*np.array(k))
        fig2, ax = plt.subplots(1, 1)
        plt.plot(paramV[start_point:end_point], mobility, marker='o', label=each_name[:-4])
        font = {'family': 'Times New Roman',
                'weight': 'normal',
                'style': 'italic',
                'size': 14
                }
        ax.semilogy()
        plt.xlabel('V$_g$ (V)', font)
        plt.ylabel('mobility (cm$^2$/V$^-$$^1$s$^-$$^1$)', font)
        plt.legend()
        plt.title(f'Mobility {each_name[:-4]}')
        plt.tight_layout()
        plt.savefig('./Data/' + f'线性区 mobility {filename} ' + each_name[:-4] + '.png', dpi=720)
        # plt.show()
        plt.close()

    print('Program end!')