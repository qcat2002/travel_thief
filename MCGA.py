import os
import initialisation as init


def get_inits(tsp_path):
    tours_200 = []
    for batch in range(5):
        target = os.path.join(tsp_path, f'batch-{batch+1}', f'tsp-{batch+1}.csv')
        tours_40 = init.read_tour(target)
        tours_200 += tours_40
    return tours_200


def algorithm(ttp_path, tsp_path):
    prob = init.read_ttp(ttp_path)
    tours_200 = get_inits(tsp_path)
    # for tour in tours_200:
    #     print(tour)
    # print(len(tours_200))
    pop_size = 200
    order_cross = 1
    n_point_cross = 1
    opt_mutate = 0.35
    bitflip_mutate = 0.825



if __name__ == '__main__':
    your_type = 1
    ttp_path_main = 'data/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp'
    tsp_path_main = os.path.join('result', 'clk_tours', f'type-{your_type}')
    algorithm(ttp_path_main, tsp_path_main)