from pathlib import Path
import os

# initialise tours or run algorithms?
work_type = {
    '1': ('初始化-路径', None),
    '2': ('运行-TTP算法', None)
}

algorithms = {
    '1': ('MCGA with CLK', None)
}

ttps = {}


def update_ttps():
    global ttps
    folder = Path(os.path.join('dataset'))
    subfolders = [f.name for f in folder.iterdir() if f.is_dir()]
    for index, name in enumerate(subfolders):
        ttps[index+1] = name

def ask_ttp():
    pass


def run():
    update_ttps()
    for key, value in work_type.items():
        print(key, value[0])
    reply = input('请选择任务：')
    if reply == '1':
        print('即将使用 CLK 初始化路径')
        print('')


run()
