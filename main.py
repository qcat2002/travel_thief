import csv
from pathlib import Path
import tool
import MCGA
import os
import re


class Problem:
    def __init__(self, dataset_name, dataset_file_name, num_city, num_item, dataset_path):
        self.dataset_name = dataset_name
        self.dataset_file_name = dataset_file_name
        self.num_city = num_city
        self.num_item = num_item
        self.dataset_path = dataset_path

    def display_problem(self):
        print(self.dataset_name)
        print(self.num_city)
        print(self.num_item)
        print(self.dataset_path)


def saver(pop, bests, algorithm, kp_type, prob, info):
    save_folder = os.path.join('result', algorithm, prob.dataset_name, str(prob.num_item), kp_type)
    print(save_folder)
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    files = [f for f in os.listdir(save_folder) if os.path.isfile(os.path.join(save_folder, f))]
    order = len(files)
    save_file_path = os.path.join(save_folder, f'result_{order+1}.csv')
    with open(save_file_path, mode='w', newline='') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(bests)
        for ind in pop:
            writer.writerow(ind.tour)
            writer.writerow(ind.kp)

def update_ttps():
    global ttps
    global details
    folder = Path(os.path.join('dataset'))
    subfolders = [f.name for f in folder.iterdir() if f.is_dir()]
    for index, name in enumerate(subfolders):
        key = str(index+1)
        ttps[key] = name
        num_city = int(''.join(re.findall(r'\d', name)))
        num_item = []
        inner_folder = os.path.join('dataset', name)
        for root, dirs, files in os.walk(inner_folder):
            for file in files:
                if file.endswith('.ttp'):
                    num = int(file.split('_')[1].replace('n', ''))
                    if num not in num_item:
                        num_item.append(num)
        num_item.sort()
        details[key] = [(num_city, some_num_items) for some_num_items in num_item]
        # print(details[key])


def ask_path():
    print('**确定目标数据集及其文件地址**')
    for key, value in ttps.items():
        print(key, value)
    reply = input('请选择数据集: ')
    dataset = ttps[reply]
    print()
    pairs = details[reply]
    for index in range(len(pairs)):
        print(index+1, pairs[index][1])
    print('如果你是在初始化-路径，请勿担心后续类型选择！(随意选择即可！)')
    reply = int(input('请选择物品数量: '))
    pair = pairs[reply-1]
    print()
    for key, value in kp_types.items():
        print(key, value)
    reply = input('请选择数据集类型: ')
    kp_type = kp_types[reply]
    print()
    print('你的选择是: ')
    part1 = dataset.split('-')[0]
    ttp_file_name = f'{part1}_n{pair[1]}_{kp_type}_01.ttp'
    print(ttp_file_name)
    file_path = os.path.abspath(os.path.join('dataset', dataset, ttp_file_name))
    prob = Problem(dataset, ttp_file_name, [0], pair[1], file_path)
    return prob, kp_type


def ask_init():
    prob, kp_type = ask_path()



def ask_algorithm():
    prob, kp_type = ask_path()
    print()
    print('**确认算法**')
    for key, value in algorithms.items():
        print(key, value[0])
    reply = input('请选择算法: ')
    alg = algorithms[reply][0]
    algorithm = algorithms[reply][1]
    info = tool.read_ttp(prob.dataset_path)
    info.dispaly_info()
    max_gen = 5000
    pop, bests = algorithm(max_gen, info)
    saver(pop, bests, alg, kp_type, prob, info)



# initialise tours or run algorithms?
work_type = {
    '1': ('初始化-路径', ask_init),
    '2': ('运行-TTP算法', ask_algorithm)
}

algorithms = {
    '1': ('MCGA', MCGA.run),
    '2': ('MCGA with CLK', None)
}

kp_types = {
    '1': 'bounded-strongly-corr',
    '2': 'uncorr-similar-weight',
    '3': 'uncorr'
}

# {1: "a280-ttp"}
ttps = {}
# {1: [(number of city, number of items)]}
details = {}


def run():
    update_ttps()
    for key, value in work_type.items():
        print(key, value[0])
    reply = input('请选择任务: ')
    work_func = work_type[reply][1]
    print()
    work_func()

if __name__ == '__main__':
    run()
