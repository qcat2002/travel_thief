import initialisation as ini
import csv
import os


def run(trial, your_type):
    path = 'data/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp'
    problem = ini.read_ttp(path)
    problem.info()
    inds = 40
    sub = 8
    rs = ini.clk(problem, inds)
    processed = 0
    runtime = 0
    # while processed < inds:
    #     seg = rs[processed:processed+sub]
    #     ini.draw(problem, seg, runtime+1)
    #     runtime += 1
    #     processed += sub

    file = os.path.join('result', 'clk_tours', f'type-{your_type}', f'batch-{trial}', f'tsp-{trial}.csv')
    if not os.path.exists(os.path.join('result', 'clk_tours', f'type-{your_type}', f'batch-{trial}')):
        os.makedirs(os.path.join('result', 'clk_tours', f'type-{your_type}', f'batch-{trial}'))
    with open(file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ')
        for row in rs:
            writer.writerow(row)


if __name__ == '__main__':
    ty = 1
    for trying in range(5):
        run(trying + 1, ty)
