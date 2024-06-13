from pathlib import Path
import os
import re

class problem:
    def __init__(self, dataset_name, num_city, num_item, dataset_path):
        self.dataset_name = dataset_name
        self.num_city = num_city
        self.num_item = num_item
        self.dataset_path = dataset_path

    def display_problem(self):
        print(self.dataset_name)
        print(self.num_city)
        print(self.num_item)
        print(self.dataset_path)

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
    ttp_file_path = f'n{pair[0]}_n{pair[1]}_{kp_type}_01.ttp'
    print(ttp_file_path)
    prob = problem(dataset, pair[0], pair[1], ttp_file_path)
    return prob


def init():
    prob = ask_path()
    prob.display_problem()


def algorithm():
    prob = ask_path()
    print()
    print('**确认算法**')
    for key, value in algorithms.items():
        print(key, value[0])
    reply = input('请选择算法: ')


# initialise tours or run algorithms?
work_type = {
    '1': ('初始化-路径', init),
    '2': ('运行-TTP算法', algorithm)
}

algorithms = {
    '1': ('MCGA', None),
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

run()
