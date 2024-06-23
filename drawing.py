import csv
import os
import main
import matplotlib.pyplot as plt
import tool


def draw_rank1(bests, times, profits, tours, kps, info):
    tour = tours[0]
    kp = kps[0]
    X = info.X
    Y = info.Y

    fig = plt.figure(figsize=(10, 10), dpi=300)
    plt.scatter(X, Y)
    # tour
    xs = []
    ys = []
    for city in tour:
        xs.append(X[city-1])
        ys.append(Y[city-1])
    xs.append(X[0])
    ys.append(Y[0])
    plt.plot(xs, ys, color='red')
    plt.show()


def read_result(result):
    with open(result, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        bests = [float(str_num) for str_num in next(reader)]
        times = [float(str_num) for str_num in next(reader)]
        profits = [float(str_num) for str_num in next(reader)]
        tours = []
        kps = []
        index = 0
        for row in reader:
            record = [int(num) for num in row]
            if index % 2 == 0:
                tours.append(record)
            else:
                kps.append(record)
            index += 1
        return bests, times, profits, tours, kps




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
    bests, times, profit, tours, kps = read_result(file)
    info = tool.read_ttp(ttp)

    return bests, times, profit, tours, kps, info


task = {
    '1': ("画最优解", draw_rank1),
    '2': ("画单目标进化趋势图", None),
    '3': ("画单多目标对比图", None)
}


def run():
    for key, value in task.items():
        print(key, value[0])
    choice = input("请选择任务: ")
    if choice == "3":
        bests_single, tours_single, kps_single, info_single = ask_info()
        bests_bi, tours_bi, kps_bi , info_bi = ask_info()
    else:
        bests, times, profits, tours, kps, info = ask_info()
        draw = task[choice][1]
        draw(bests, times, profits, tours, kps, info)


if __name__ == '__main__':
    run()