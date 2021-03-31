import csv
from openpyxl import load_workbook
import matplotlib.pyplot as plt
import numpy as np
import os
import math


def load_files(path='/Users/mac/Documents/Data/'):
    '''

    :param path:
    :return: files
    '''

    input_extension = input('请输入数据文件格式(xlsx或者CSV)：')
    # 分别存储后缀名为xlsx, csv的文件名称
    files_xlsx = []
    files_csv = []
    output_names = []
    if input_extension == 'xlsx':
        # 读取 path 下的所有文件的文件名
        files_name = os.listdir(path + 'Excel/')
        # print(files_name)
        # 根据后缀名筛选出xlsx文件
        for each in files_name:
            files_extension = os.path.splitext(each)[1]
            # print(files_extension)
            if files_extension == '.xlsx':
                files_xlsx.append(each)
        output_names = files_xlsx.copy()
    elif input_extension == 'CSV':
        # 读取 path 下的所有文件的文件名
        files_name = os.listdir(path + 'CSV/')
        # print(files_name)
        # 根据后缀名筛选出xlsx文件
        for each in files_name:
            files_extension = os.path.splitext(each)[1]
            # print(files_extension)
            if files_extension == '.csv':
                files_xlsx.append(each)
        output_names = files_csv.copy()
    return output_names

