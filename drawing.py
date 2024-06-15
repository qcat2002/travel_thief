import csv
import os
import main

def draw_route():
    pass


def read_result(result):
    with open(result, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        bests = [float(str_num) for str_num in next(reader)]



def search_file(folder):
    return [name for name in os.listdir(folder) if os.path.isdir(os.path.join(folder, name))]


def ask_info():
    main.update_ttps()
    for key, value in main.algorithms.items():
        print(key, value[0])
    algorithm = main.algorithms[input("请选择对应算法: ")][0]
    for key, value in main.ttps.items():
        print(key, value)
    dataset = main.ttps[input("请选择对应数据集: ")]
    temp_folder = os.path.join('result', algorithm, dataset)
    if not os.path.exists(temp_folder):
        print("从未实验过！")
        return
    subfolders = search_file(temp_folder)
    if len(subfolders) == 0:
        print("没有结果！")
        return
    for index in range(len(subfolders)):
        print(index+1, subfolders[index])
    num_item = subfolders[int(input("请选择物品数量: "))-1]
    temp_folder = os.path.join(temp_folder, num_item)
    subfolders = search_file(temp_folder)
    if len(subfolders) == 0:
        print("没有结果！")
        return
    for index in range(len(subfolders)):
        print(index+1, subfolders[index])
    kp_type = subfolders[int(input("请选择关系种类: "))-1]
    temp_folder = os.path.join(temp_folder, kp_type)
    subfiles = [f for f in os.listdir(temp_folder) if os.path.isfile(os.path.join(temp_folder, f))]
    if len(subfiles) == 0:
        print("没有结果！")
        return
    for index in range(len(subfiles)):
        print(index+1, subfiles[index])
    trial = subfiles[int(input("请选择对应文件: "))-1]

    file = os.path.join(temp_folder, trial)
    ttp_city = dataset.split('-')[0]
    ttp = os.path.join('dataset', dataset, f'{ttp_city}_n{num_item}_{kp_type}_01.ttp')
    # read result file
    read_result(file)



ask_info()