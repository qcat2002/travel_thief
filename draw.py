import initialisation
import csv
import os

def draw(prob, routes, timer, save):
    import matplotlib.pyplot as plt
    row = 2
    col = 4
    fig, axes = plt.subplots(nrows=row, ncols=col, figsize=(24, 12), dpi=300)

    # 假设您有一个名为 prob 的对象，其中包含 X 和 Y 坐标
    # 您需要将 prob.X 和 prob.Y 替换为您的实际数据
    colors = ['orange', (135 / 255, 206 / 255, 250 / 255)]
    indicator = 0
    for x in range(row):
        for y in range(col):
            axes[x, y].scatter(prob.X, prob.Y, color='black')  # 在每个子图上绘制散点图
            axes[x, y].tick_params(axis='both', which='major', labelsize=18, width=3, length=6)  # 设置刻度标签的样式
            xs = []
            ys = []
            for index in range(len(routes[indicator])):
                xs.append(prob.X[routes[indicator][index]])
                ys.append(prob.Y[routes[indicator][index]])
            xs.append(prob.X[routes[indicator][0]])
            ys.append(prob.Y[routes[indicator][0]])
            axes[x, y].plot(xs, ys, color=colors[x % len(colors)])
            indicator += 1
    # else:
    #     for y in range(col):
    #         axes[y].scatter(prob.X, prob.Y)
    #         axes[y].tick_params(axis='both', which='major', labelsize=18, width=3, length=6)

    if not os.path.exists(save):
        os.makedirs(save)
    fig.suptitle(f'clk_tours-trials{((timer - 1) * 8) + 1}~{timer * 8}', fontsize=26, fontweight='bold')
    plt.tight_layout()
    plt.savefig(os.path.join(save, f'clk_tours-{timer}.png'))
    plt.show()

def run(path, your_type):
    sub = 8
    prob = initialisation.read_ttp(path)
    target = os.path.join('result', 'clk_tours', f'type-{your_type}')
    for batch in range(5):
        file = os.path.join(target, f'batch-{batch + 1}', f'tsp-{batch + 1}.csv')
        tours = initialisation.read_tour(file)
        processed = 0
        runtime = 0
        while processed < len(tours):
            seg = tours[processed:processed + sub]
            draw(prob, seg, runtime+1, os.path.join(target, f'batch-{batch + 1}'))
            runtime += 1
            processed += sub


if __name__ == '__main__':
    ttp_path = 'data/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp'
    ty = 1
    run(ttp_path, ty)
