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

def draw_graph_csv(x, y, csvname, delt_x=20):

    # 利用导入的csv数据生成设定好的图像（一个）
    fig, ax = plt.subplots(1, 1)

    # 刻度调整为朝内
    # plt.rcParams['xtick.direction'] = 'out'  # 将x轴的刻度方向设置向内
    # plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

    # 设置图像标识
    plt.plot(x, y, linestyle='--', color='green', marker='o')

    # 自动根据导入数据设置横坐标范围，取整然后左右移动5个单位
    plt.xlim([int(min(x))-5, int(max(x))+5])

    # 自动根据导入数据设置纵坐标范围，
    temp_min = 10**(math.log(min(y), 10) - 1)
    temp_max = 10**(math.log(max(y), 10) + 1)
    plt.ylim([temp_min, temp_max])
    my_x_ticks = np.arange(int(min(x)), int(max(x)) + delt_x, delt_x)
    plt.xticks(my_x_ticks)

    # 纵轴修改为对数形式
    ax.semilogy()

    # 设定图像的轴坐标字体样式
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'style': 'italic',
             'size': 14
             }
    plt.xlabel('V$_g$ (V)', font1)
    plt.ylabel('-I$_s$$_d$ (A)', font1)

    # 设定图像标题
    plt.title(csvname[:-4])

    # 这里的参数更改为图像存放位置
    # split(str='', num=) str为分割位置，num=1为将字符串分割为两份
    # plt.savefig('./Output/' + csvname[:-4] + '.png', dpi=720)
    plt.show()
    plt.close()
    return 0

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

def cut_line(x, k, x0, y0):
    y = k*(x - x0) + y0
    return y


if __name__ == '__main__':

    csv_name = load_files()
    csv_name.sort()
    filename = '20220526 DPP-DTT 2.3'

    e=1.6e-19
    L=3e-4 # 300μm
    W=3e-3 # 3mm
    C=11.9e-9 # F
    Vsd=-5 # V
    d=1e-8 # 10nm
    edging_times = len(csv_name)
    delta_d = d/edging_times

    V_range = np.array([])
    point_pick = 30 # 取值 30
    start_point = 0
    end_point = 60

    k = dict()
    k_list = []

    G = dict()
    G_list = []

    n = dict()
    n_list = []

    N = dict()
    N_list = []

    mobility = dict()
    mobility_list = []

    i = 0
    A_list = []
    B = abs(L/(W*C*Vsd))

    for each_name in csv_name:
        A = abs(L / (W * (d-i*delta_d) * e))
        A_list.append(A)
        paramV, paramI, data = load_csv_data(each_name)
        V_range = paramV

        k[each_name[:-4]]=abs(cal_deriv(paramV[:end_point], paramI[:end_point])[point_pick])
        k_list.append(float(k[each_name[:-4]]))

        mobility[each_name[:-4]] = B*k[each_name[:-4]]
        mobility_list.append(mobility[each_name[:-4]])

        G[each_name[:-4]] = abs(paramI[:end_point][point_pick]/Vsd)
        G_list.append(G[each_name[:-4]])

        n[each_name[:-4]] = A*G[each_name[:-4]]/mobility[each_name[:-4]]
        n_list.append(n[each_name[:-4]])

        N[each_name[:-4]] = n[each_name[:-4]] * (d-i*delta_d)
        N_list.append(N[each_name[:-4]])

        i += 1
        plt.plot(paramV[start_point:end_point], paramI[start_point:end_point], label=each_name[:-4])
    plt.axvline(x=V_range[point_pick], ls='--', c='red')
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
    plt.savefig('./Data/' + f'线性区 Trans_Curve {filename}' + '.png', dpi=720)
    plt.show()

    # 断层计算：电导，迁移率，电荷密度，总电荷量
    plt.subplot(2, 2, 1)
    plt.plot(G_list, label='G')
    plt.legend()
    plt.subplot(2, 2, 2)
    plt.plot(mobility_list, label='mobility')
    plt.legend()
    plt.subplot(2, 2, 3)
    plt.plot(n_list, label='n')
    plt.legend()
    plt.subplot(2, 2, 4)
    plt.plot(N_list, label='N')
    plt.legend()
    plt.tight_layout()
    plt.savefig('./data/断层迁移率计算（电导，迁移率，电荷密度，总电荷量）.png', dpi=720)
    plt.show()

    text_save('断层迁移率计算 电导.txt', G_list)
    text_save('断层迁移率计算 迁移率.txt', mobility_list)
    text_save('断层迁移率计算 电荷密度.txt', n_list)
    text_save('断层迁移率计算 总电荷量.txt', N_list)

