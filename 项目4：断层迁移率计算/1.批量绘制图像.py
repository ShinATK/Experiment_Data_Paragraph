import csv
import matplotlib.pyplot as plt
import numpy as np
import os


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


if __name__ == '__main__':

    csv_name = load_files()
    csv_name.sort()
    filename = '20220517 PCDTPT Point 1'

    for each_name in csv_name:

        paramV, paramI, data = load_csv_data(each_name)

        plt.plot(paramV[40:50], paramI[40:50], label=each_name[:-4])

    font = {'family': 'Times New Roman',
             'weight': 'normal',
             'style': 'italic',
             'size': 14
             }
    plt.xlabel('V$_g$ (V)', font)
    plt.ylabel('-I$_s$$_d$ (A)', font)
    plt.legend()
    # plt.title(each_name[:-4])
    plt.tight_layout()
    # plt.savefig('./Data/' + f'线性区 {filename}' + '.png', dpi=720)
    plt.show()
