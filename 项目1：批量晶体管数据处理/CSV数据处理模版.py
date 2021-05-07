import csv
import matplotlib.pyplot as plt
import numpy as np
import os
import math

def load_files(path='./Data/CSV/'):
    '''

    :param path:
    :return: files_csv
    '''

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

    return files_csv

def load_csv_data(filename, path='./Data/CSV/'):
    load_file_csv = open(path + filename) # 打开csv文件
    read_file_csv = csv.reader(load_file_csv) # 读取csv文件
    data = list(read_file_csv)

    x_Voltage = list()
    y_Current = list()

    for i in range(1, 82):
        x_Voltage.append(float(data[i][6]))
        y_Current.append(abs(float(data[i][4])))

    return x_Voltage, y_Current

def draw_graph_csv(x, y, csvname, delt_x=20):

    # 利用导入的csv数据生成设定好的图像（一个）
    fig, ax = plt.subplots(1, 1)

    # 刻度调整为朝内
    # plt.rcParams['xtick.direction'] = 'out'  # 将x轴的刻度方向设置向内
    # plt.rcParams['ytick.direction'] = 'in'  # 将y轴的刻度方向设置向内

    plt.plot(x, y, linestyle='--', color='green', marker='o')

    plt.xlim([int(min(x))+5, int(max(x))+5])

    temp_min = 10**(math.log(min(y), 10) - 1)
    temp_max = 10**(math.log(max(y), 10) + 1)

    plt.ylim([temp_min, temp_max])

    my_x_ticks = np.arange(int(min(x)), int(max(x)) + delt_x, delt_x)
    plt.xticks(my_x_ticks)

    # 纵轴修改为对数形式
    ax.semilogy()

    # 设定图像的轴坐标名称
    font1 = {'family': 'Times New Roman',
             'weight': 'normal',
             'style': 'italic',
             'size': 14
             }

    plt.xlabel('V$_g$$_s$ (V)', font1)
    plt.ylabel('-I$_s$$_d$ (A)', font1)

    # 设定图像标题
    plt.title(csvname[0:-4])

    # 这里的参数更改为图像存放位置
    plt.savefig('./Fig/CSV_Fig/' + csvname.split('.', 1)[0] + '.png', dpi=720)
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

if __name__ == '__main__':

    # file_name = load_files()
    # load_file_csv = open('/Users/mac/Documents/Data/CSV/20201231_1_1.csv')
    # read_file_csv = csv.reader(load_file_csv)
    # data_file_csv = list(read_file_csv)
    # for i in range(1, 82):
    #     print('%e' %float(data_file_csv[i][4]))
    csv_name = load_files()
    for each_name in csv_name:
        param1, param2 = load_csv_data(each_name)
        paramI = []
        # u = []
        for each_I in param2[10:41]:
            paramI.append(math.sqrt(each_I))
        # 电流开根号，对电压取微分，乘10000，平方后再除以5，选取第一遍扫的结果，选取其中最大值
        # for each in cal_deriv(param1[0:41], paramI):
        #    u.append((each * 10000)**2 / 5)

        deriv = []
        for each_result in cal_deriv(param1[10:41], paramI):
            deriv.append(abs(each_result))
        deriv.sort(reverse=True)
        # print(deriv[0])
        u = []
        for each_deriv in deriv:
            u.append((each_deriv * 10000) ** 2 / 5)
        # u = (deriv[0]*10000)**2 / 5
        # for each in u:
        #    print(each)

        # 计算得到的平均迁移率会与最大值有过大的偏差，此方法不可取
        # sum = 0
        # for each in u:
        #     sum += each
        # ave = sum/len(u)
        # print('平均迁移率为：%0.2f' %ave)

        param1_I = param2.copy()
        param1_I.sort(reverse=True)
        param2_I = param2[10:41].copy()
        param2_I.sort(reverse=True)

        I_onoff = []
        I_onoff.append(math.log(param2_I[0] / param2_I[-1], 10))

        I_onoff.append(math.log(param1_I[0] / param1_I[-1], 10))
        I_onoff.append(math.log(param1_I[0] / param1_I[-2], 10))
        I_onoff.append(math.log(param1_I[0] / param1_I[-3], 10))
        I_onoff.append(math.log(param1_I[0] / param1_I[-4], 10))
        # u.sort(reverse=True)
        # 迁移率具体数值与直接用origin计算得出的结果相差一倍，无法定量分析，但是不同片子的迁移率之间相对优劣的定性分析是可行的
        print(each_name + '前三组迁移率为:%0.2f; %0.2f, %0.2f, %0.2f, %0.2f'
              % (u[0], u[1], u[2], u[3], u[4]))
        print(each_name + '开关比为：%0.2f; %0.2f, %0.2f, %0.2f, %0.2f \n'
              % (I_onoff[0], I_onoff[1], I_onoff[2], I_onoff[3], I_onoff[4]))

        draw_graph_csv(param1, param2, each_name)


