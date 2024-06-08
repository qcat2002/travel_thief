import os
import initialisation as init
import encode


def get_inits(tsp_path):
    tours_200 = []
    for batch in range(5):
        target = os.path.join(tsp_path, f'batch-{batch+1}', f'tsp-{batch+1}.csv')
        tours_40 = init.read_tour(target)
        tours_200 += tours_40
    return tours_200


def violate(prob, ind):
    print('old', ind.vio)
    weight = 0
    for index in range(len(ind.kp)):
        if ind.kp[index] == 1:
            weight += prob.weight[index]
    ind.weight = weight
    if weight > prob.W:
        ind.vio = True
    else:
        ind.vio = False
    print('new', ind.vio)
    print()

def repair(prob, ind):
    pass

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

    item_id_at_city = {}
    for city_id in prob.city_ID:
        items = []
        for index in range(len(prob.item_ID)):
            if city_id == prob.belongto[index]:
                items.append(prob.item_ID[index])
        item_id_at_city[city_id] = items

    kp = [0] * len(prob.item_ID)

    pop = []
    for indicator in range(pop_size):
        ind = encode.Ind(tours_200[indicator], kp)
        violate(prob, ind)
        pop.append(ind)
    print(len(pop))


if __name__ == '__main__':
    your_type = 1
    ttp_path_main = 'data/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp'
    tsp_path_main = os.path.join('result', 'clk_tours', f'type-{your_type}')
    algorithm(ttp_path_main, tsp_path_main)