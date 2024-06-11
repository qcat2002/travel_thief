import csv
import os
import initialisation as init
import encode
import random
import time


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
    # print(ratio)
    while ind.vio:
        id = ratio[0][0]
        ind.kp[id-1] = 0
        violate(prob, ind)
        ratio = ratio[1:]
    # print(ind.kp)
    # print(ind.weight, prob.W)
    # print()


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
    ind.fitness = profit - (prob.R * time)


def order_sort(sort_list, reference):
    new_list = []
    for elem in sort_list:
        for index in range(len(reference)):
            if reference[index] == elem:
                new_list.append((elem, index))
    return new_list

def crossover(p1, p2, order, n_point):
    tsp1 = p1.tour[1:]
    tsp2 = p2.tour[1:]
    if random.random() < order:
        length = len(tsp1)
        # order crossover
        masked = [random.choice([0, 1]) for ccc in range(length)]
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
        b1 = sorted(order_sort(b1, tsp2), key=lambda x: x[1])
        b2 = sorted(order_sort(b2, tsp1), key=lambda x: x[1])
        counter = 0
        for index in range(len(tsp1)):
            if masked[index] == 0:
                new_tsp1[index] = b1[counter][0]
                new_tsp2[index] = b2[counter][0]
                counter += 1
        new_tsp1 = [0] + new_tsp1
        new_tsp2 = [0] + new_tsp2
    else:
        new_tsp1 = [0] + tsp1
        new_tsp2 = [0] + tsp2

    # N-point crossover
    kp1 = p1.kp[:]
    kp2 = p2.kp[:]
    if random.random() < n_point:
        length = len(kp1)
        crossover_points = [0] + sorted(random.sample(range(1, length), 3)) + [length]
        new_kp1 = []
        new_kp2 = []
        for ii in range(len(crossover_points)-1):
            start = crossover_points[ii]
            end = crossover_points[ii+1]
            if ii % 2 == 0:
                new_kp1.extend(kp1[start:end])
                new_kp2.extend(kp2[start:end])
            else:
                new_kp1.extend(kp2[start:end])
                new_kp2.extend(kp1[start:end])
    else:
        new_kp1 = kp1
        new_kp2 = kp2
    # print(kp1[crossover_points[1]:crossover_points[2]])
    # print(new_kp2[crossover_points[1]:crossover_points[2]])
    c1 = encode.Ind(new_tsp1, new_kp1)
    c2 = encode.Ind(new_tsp2, new_kp2)
    return c1, c2


def opt(list):
    selected_points = sorted(random.sample(range(0, len(list)), 2))
    # print(selected_points)
    new_list = list[:selected_points[0]] + list[selected_points[0]:selected_points[1]][::-1] + list[selected_points[1]:]
    return new_list

def bitflip(kp, p):
    new_kp = []
    for elem in kp:
        if random.random() < p:
            new_kp.append((elem+1)%2)
        else:
            new_kp.append(elem)
    return new_kp

def algorithm(ttp_path, tsp_path):
    debug = True
    start = time.time()
    prob = init.read_ttp(ttp_path)
    tours_200 = get_inits(tsp_path)
    # for tour in tours_200:
    #     print(tour)
    # print(len(tours_200))
    pop_size = 200
    max_gen = 30000
    # max_gen = 100
    num_elite = 12
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

    if debug:
        kp = [random.choice([0, 1]) for _ in range(len(prob.item_ID))]
    else:
        kp = [0] * len(prob.item_ID)

    pop = []
    for indicator in range(pop_size):
        if debug:
            random.shuffle(kp)
            ind = encode.Ind(tours_200[indicator][:], kp[:])
        else:
            ind = encode.Ind(tours_200[indicator][:], kp[:])
        violate(prob, ind)
        if ind.vio:
            repair(prob, ind)
        evaluate(prob, item_id_at_city, ind)
        pop.append(ind)

    bests = []
    for gen in range(max_gen):
        old_pop = pop[:]
        old_pop = sorted(old_pop, key=lambda x: x.fitness, reverse=True)
        elites = old_pop[:num_elite]
        bests.append(elites[0].fitness)
        print(gen, elites[0].fitness)

        parents = []
        while len(parents) <= pop_size:
            candidates = random.sample(old_pop, 2)
            selected = max(candidates, key=lambda x: x.fitness)
            parents.append(selected.copy())

        i = 0
        j = 1
        offspring = []
        while j < len(parents):
            p1 = parents[i]
            p2 = parents[j]
            c1, c2 = crossover(p1, p2, order_cross, n_point_cross)
            offspring.append(c1)
            offspring.append(c2)
            i += 2
            j += 2

        for child in offspring:
            violate(prob, child)
            if child.vio:
                repair(prob, child)
            evaluate(prob, item_id_at_city, child)
        # merge
        new_large_pop = parents + offspring
        # environment selection! elites will automatically join into next Gen
        next_gen = []
        bound = pop_size - num_elite
        while len(next_gen) < bound:
            candidates = random.sample(new_large_pop, 2)
            selected = max(candidates, key=lambda x: x.fitness)
            next_gen.append(selected.copy())

        # mutate
        for ind in next_gen:
            mutate = False
            if random.random() < opt_mutate:
                mutate = True
                tsp = ind.tour[1:]
                mutated_tsp = opt(tsp)
                ind.tour = [0] + mutated_tsp
            if random.random() < bitflip_mutate:
                mutate = True
                this_kp = ind.kp[:]
                mutated_kp = bitflip(this_kp, 0.2)
                ind.kp = mutated_kp
            if mutate:
                violate(prob, ind)
                if ind.vio:
                    repair(prob, ind)
                evaluate(prob, item_id_at_city, ind)
        # merge elites
        pop = next_gen + elites

    end = time.time()
    print('时间：', str(end - start))
    return pop, bests, prob


def save(pop, bests, prob, path):
    sorted_pop = sorted(pop, key=lambda x: x.fitness, reverse=True)
    bests.append(sorted_pop[0].fitness)
    with open(path, 'w') as f:
        writer = csv.writer(f, delimiter=' ')
        writer.writerow(['name', prob.name])
        writer.writerow(['KP-Type', f'{prob.KP_type}'])
        writer.writerow(bests)
        for ind in sorted_pop:
            route = [str(city+1) for city in ind.tour]
            writer.writerow(route)
            kp = [str(pick) for pick in ind.kp]
            writer.writerow(kp)
            writer.writerow(['fitness', round(ind.fitness), 'time', round(ind.time), 'profit', round(ind.profit)])


if __name__ == '__main__':
    your_type = 2
    ttp_path_main = 'data/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp'
    tsp_path_main = os.path.join('result', 'clk_tours', f'type-{your_type}')
    finish_population, bests, problem = algorithm(ttp_path_main, tsp_path_main)

    trial = 1
    save_folder = os.path.join('result', 'mcga', 'a280-ttp')
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    save_path = os.path.join(save_folder, f'trial-{trial}')
    save(finish_population, bests, problem, save_path)