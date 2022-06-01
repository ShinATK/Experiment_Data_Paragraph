import os

path_set = 'Data/'

def load_files(path=path_set):
    # 读取 path 下的所有文件的文件名
    files_name = os.listdir(path)

    # 存储后缀名为csv的文件名称
    files_csv = []
    files_extension = '.csv' # 默认为csv文件

    # 根据后缀名筛选出csv文件
    for each in files_name:
        files_extension = os.path.splitext(each)[1]
        # print(files_extension)
        if files_extension == '.csv':
            files_csv.append(os.path.splitext(each)[0])
    # 按文件名排序
    files_csv.sort()
    return files_csv, files_extension


def get_folder_name():
    folder_name = os.listdir(path_set)
    for each in folder_name:
        if os.path.isdir(path_set+each):
            pass
        else:
            folder_name.remove(each)
    folder_name.sort()
    return folder_name

def re_name_func(origin_name, folder_name, files_extension):

    os.rename(f"{path_set}{folder_name}/{origin_name}{files_extension}",
              f"{path_set}{folder_name}/{origin_name}_{folder_name}{files_extension}")

    return 0

if __name__ == '__main__':

    folder_name = get_folder_name()

    for each_folder in folder_name:
        name_list, files_extension = load_files(f'Data/{each_folder}/')
        for each in name_list:
            re_name_func(each, each_folder, files_extension)
    print('Done!')