import os
import initialisation as init
import encode
import random


def get_inits(tsp_path):
    tours_200 = []
    for batch in range(5):
        target = os.path.join(tsp_path, f'batch-{batch+1}', f'tsp-{batch+1}.csv')
        tours_40 = init.read_tour(target)
        tours_200 += tours_40
    return tours_200


def violate(prob, ind):
    weight = 0
    for index in range(len(ind.kp)):
        if ind.kp[index] == 1:
            weight += prob.weight[index]
    ind.weight = weight
    if weight > prob.W:
        ind.vio = True
    else:
        ind.vio = False


def repair(prob, ind):
    picked_id = []
    profit = []
    weight = []
    for index in range(len(ind.kp)):
        if ind.kp[index] == 1:
            picked_id.append(prob.item_ID[index])
            profit.append(prob.profit[index])
            weight.append(prob.weight[index])
    # print(picked_id)
    # print(profit)
    # print(weight)
    ratio = sorted([(picked_id[c], profit[c]/weight[c]) for c in range(len(picked_id))], key=lambda x: x[1])
    print(ratio)
    while ind.vio:
        id = ratio[0][0]
        ind.kp[id-1] = 0
        violate(prob, ind)
        ratio = ratio[1:]
    # print(ind.kp)
    # print(ind.weight, prob.W)
    print()


def evaluate(prob, item_id_at_city, ind):
    profit = 0
    weight = 0
    time = 0
    v = (prob.max_speed - prob.min_speed) / prob.W
    for index in range(len(ind.tour)-1):
        this_city = ind.tour[index]
        next_city = ind.tour[index+1]
        # print(this_city, next_city)
        distance = prob.dist[this_city][next_city]
        items = item_id_at_city[this_city]
        for item_id in items:
            if ind.kp[item_id-1] == 1:
                profit += prob.profit[item_id-1]
                weight += prob.weight[item_id-1]
        time += distance / (prob.max_speed - (v * weight))

    distance = prob.dist[ind.tour[-1]][0]
    items = item_id_at_city[ind.tour[-1]]
    for item_id in items:
        if ind.kp[item_id - 1] == 1:
            profit += prob.profit[item_id - 1]
            weight += prob.weight[item_id - 1]
    time += distance / (prob.max_speed - (v * weight))
    ind.profit = profit
    ind.time = time
    ind.fitness = profit - (prob.W * time)



def algorithm(ttp_path, tsp_path):
    prob = init.read_ttp(ttp_path)
    tours_200 = get_inits(tsp_path)
    # for tour in tours_200:
    #     print(tour)
    # print(len(tours_200))
    pop_size = 200
    max_gen = 100
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
        item_id_at_city[city_id-1] = items

    kp = [0] * len(prob.item_ID)

    pop = []
    for indicator in range(pop_size):
        ind = encode.Ind(tours_200[indicator][:], kp[:])
        violate(prob, ind)
        if ind.vio:
            repair(prob, ind)
        evaluate(prob, item_id_at_city, ind)
        pop.append(ind)

    for gen in range(max_gen):
        old_pop = pop[:]
        old_pop = sorted(old_pop, key=lambda x: x.fitness, reverse=True)
        elites = old_pop[:12]

        parents = []
        while len(parents) <= pop_size:
            candidates = random.sample(old_pop, 2)
            parents.append(max(candidates, key=lambda x: x.fitness))
        print([ind.fitness for ind in parents])

        i = 0
        j = 1
        offspring = []
        while j < len(parents):
            p1 = parents[i]
            p2 = parents[j]
            tsp1 = p1.tour[:]
            tsp2 = p2.tour[:]
            length = len(tsp1)
            # order crossover
            masked = [random.choice([0,1]) for ccc in range(length)]
            new_tsp1 = [-1] * length
            new_tsp2 = [-1] * length
            b1 = []
            b2 = []
            for index in range(len(tsp1)):
                if masked[index] == 1:
                    new_tsp1[index] = tsp1[index]
                    new_tsp2[index] = tsp2[index]
                else:
                    b1.append(tsp1[index])
                    b2.append(tsp2[index])
            # print('a', b1)
            # print('b', b2)
            i += 2
            j += 2


if __name__ == '__main__':
    your_type = 1
    ttp_path_main = 'data/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp'
    tsp_path_main = os.path.join('result', 'clk_tours', f'type-{your_type}')
    algorithm(ttp_path_main, tsp_path_main)