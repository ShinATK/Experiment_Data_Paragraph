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
    filename = '20220526 DPP-DTT 2.2'

    i = 0

    e=1.6e-19
    L=3e-4 # 300μm
    W=3e-3 # 3mm
    C=11.9e-9 # F
    Vsd=-5 # V
    d=1e-8 # 10nm

    # edging_times = len(csv_name)
    edging_times = len(csv_name)-1

    end_time = 5*len(csv_name)
    delta_d = d/edging_times

    k=dict()
    k_list=[]

    G=dict()
    G_list=[]
    G_layer=[]

    n=dict()
    n_list=[]
    n_layer=[]

    N=dict()
    N_list=[]
    N_layer=[]

    sigma=dict()
    sigma_list=[]

    mobility=dict()
    mobility_list=[]
    mobility_layer=[]

    V_range = np.array([])
    point_pick = 30 # 取值 30
    start_point = 0
    end_point = 60

    for each_name in csv_name:

        paramV, paramI, data = load_csv_data(each_name)
        V_range = paramV

        k[each_name[:-4]] = cal_deriv(paramV[:end_point], paramI[:end_point])[point_pick]
        k_list.append(float(k[each_name[:-4]]))

        A = L*1e-4 / (W * C * Vsd)
        mobility[each_name[:-4]]=abs(A*k[each_name[:-4]])
        mobility_list.append(float(mobility[each_name[:-4]]))

        G[each_name[:-4]] = abs(paramI[:end_point][point_pick] / Vsd)
        G_list.append(G[each_name[:-4]])

        sigma[each_name[:-4]] = G[each_name[:-4]] * L / (W*((d-i*delta_d)))
        sigma_list.append(sigma[each_name[:-4]])

        N[each_name[:-4]] = L**2*G[each_name[:-4]] / (e * mobility[each_name[:-4]])
        N_list.append(N[each_name[:-4]])

        n[each_name[:-4]] = sigma[each_name[:-4]] / (e * mobility[each_name[:-4]])
        n_list.append(n[each_name[:-4]])

        i += 1

        # plt.plot(paramV[35:45], paramI[35:45], label=each_name[:-4])
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

    # 这里的计算过程需要修改
    for i in range(len(N_list)-1):
        N_layer.append(abs(N_list[i]-N_list[i+1]))
        G_layer.append(abs(G_list[i]-G_list[i+1]))
        mobility_layer.append(L**2*G_layer[-1]/(e*N_layer[-1]))

        n_layer.append(abs(N_layer[-1]/(W*L*delta_d)))

    t1=range(0, end_time, 5)

    plt.subplot(2, 2, 1)
    plt.plot(t1, G_list, label='G')
    plt.legend()
    plt.xticks(t1)
    plt.subplot(2, 2, 2)
    plt.plot(t1, [each*1e4 for each in mobility_list], label='mobility(cm$^2$V$^-$$^1$s$^-$$^1$)')
    plt.legend()
    plt.xticks(t1)
    plt.subplot(2, 2, 3)
    plt.plot(t1, N_list, label='N')
    plt.legend()
    plt.xticks(t1)
    plt.subplot(2, 2, 4)
    plt.plot(t1, n_list, label='n')
    plt.legend()
    plt.suptitle('Linear region each left')
    plt.xticks(t1)
    plt.tight_layout()
    plt.savefig('./Data/' + f'线性区 each_left {filename}' + '.png', dpi=720)
    plt.show()

    t2=range(1, len(csv_name))
    plt.subplot(2, 2, 1)
    plt.plot(t2, G_layer, label='G_layer')
    plt.legend()
    plt.xticks(t2)
    plt.subplot(2, 2, 2)
    plt.plot(t2, [each*1e4 for each in mobility_layer], label='mobility_layer(cm$^2$V$^-$$^1$s$^-$$^1$)')
    plt.legend()
    plt.xticks(t2)
    plt.subplot(2, 2, 3)
    plt.plot(t2, N_layer, label='N_layer')
    plt.legend()
    plt.xticks(t2)
    plt.subplot(2, 2, 4)
    plt.plot(t2, n_layer, label='n_layer')
    plt.legend()
    plt.xticks(t2)
    plt.suptitle('Linear region each layer')
    plt.tight_layout()
    plt.savefig('./Data/' + f'线性区 each_layer {filename}' + '.png', dpi=720)
    plt.show()
