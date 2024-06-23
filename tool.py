import random
import csv
import math
import multiprocessing as mp


class Information:
    def __init__(self):
        self.name = ''
        self.KP_type = ''
        self.total_cities = 0
        self.total_items = 0
        self.W = 0
        self.min_speed = 0.00
        self.max_speed = 0.00
        self.R = 0.00
        self.city_ID = []
        self.X = []
        self.Y = []
        self.item_ID = []
        self.profit = []
        self.weight = []
        self.belongto = []
        self.dist = [[]]

    def dispaly_info(self):
        print('==================================')
        print('问题的收录信息: ')
        print(f'问题名称：{self.name}')
        print(f'KP类型：{self.KP_type}')
        print(f'城市数量：{self.total_cities}')
        print(f'物品数量：{self.total_items}')
        print(f'最大重量：{self.W}')
        print(f'最小速度：{self.min_speed}')
        print(f'最大速度：{self.max_speed}')
        print(f'租金：{self.R}')
        print('==================================')
        # print('城市信息列表 (ID, X, Y)')
        # for index in range(self.total_cities):
        #     print(f'ID: {self.city_ID[index]:<5} X: {self.X[index]:<8} Y: {self.Y[index]:<8}')
        # print('==================================')
        # print('物品信息列表 (ID, profit, weight, which city?)')
        # for index in range(self.total_items):
        #     print(
        #         f'ID: {self.item_ID[index]:<5} profit: {self.profit[index]:<8} weight: {self.weight[index]:<8} city_ID:{self.belongto[index]:<5}')
        # print('==================================')
        # for row_elem in self.dist:
        #     chain = ''
        #     for col_elem in row_elem:
        #         chain += f'{str(col_elem):<35}'
        #     print(chain)
        # print(len(self.dist), len(self.dist[0]))

class Individual:
    def __init__(self, tour, kp):
        self.tour = tour
        self.kp = kp
        self.violate = True
        # single-objective
        self.fitness = -1
        self.weight = 0
        # bi-objective
        self.profit = 0
        self.time = 0

    def copying(self):
        new_ind = Individual(self.tour, self.kp)
        new_ind.violate = self.violate
        new_ind.fitness = self.fitness
        new_ind.weight = self.weight
        new_ind.profit = self.profit
        new_ind.time = self.time
        return new_ind


def read_ttp(path):
    debug = False  # debug indicator

    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        info = Information()
        info.name = next(reader)[1]
        info.KP_type = next(reader)[0].split(': ')[1]
        info.total_cities = int(next(reader)[1])
        info.total_items = int(next(reader)[1])
        info.W = int(next(reader)[1])
        info.min_speed = float(next(reader)[1])
        info.max_speed = float(next(reader)[1])
        info.R = float(next(reader)[1])

        next(reader)
        next(reader)

        for _ in range(info.total_cities):
            city = [float(number) for number in next(reader)]
            info.city_ID.append(int(city[0]))
            info.X.append(city[1])
            info.Y.append(city[2])

        next(reader)

        for _ in range(info.total_items):
            item = [int(number) for number in next(reader)]
            info.item_ID.append(item[0])
            info.profit.append(item[1])
            info.weight.append(item[2])
            info.belongto.append(item[3])

        info.dist = [([0.00] * info.total_cities) for _ in range(info.total_cities)]
        if debug:
            for row in range(info.total_cities):
                for col in range(info.total_cities):
                    info.dist[row][col] = ([row + 1, col + 1],
                                           math.sqrt(
                                               (info.X[row] - info.X[col]) ** 2 + (info.Y[row] - info.Y[col]) ** 2))
        else:
            for row in range(info.total_cities):
                for col in range(info.total_cities):
                    info.dist[row][col] = math.sqrt(
                        (info.X[row] - info.X[col]) ** 2 + (info.Y[row] - info.Y[col]) ** 2)

        return info


def tournament(pop, number_of_individuals):
    parents = []
    while len(parents) < number_of_individuals:
        candidates = random.sample(pop, 2)
        parents.append(max(candidates, key=lambda x: x.fitness))
    return parents


def violate(info, ind):
    weight = 0
    for index in range(len(ind.kp)):
        if ind.kp[index] == 1:
            weight += info.weight[index]
    ind.weight = weight
    if weight > info.W:
        ind.vio = True
    else:
        ind.vio = False


def repair(info, ind):
    picked_id = []
    profit = []
    weight = []
    for index in range(len(ind.kp)):
        if ind.kp[index] == 1:
            picked_id.append(info.item_ID[index])
            profit.append(info.profit[index])
            weight.append(info.weight[index])
    # print(picked_id)
    # print(profit)
    # print(weight)
    ratio = sorted([(picked_id[c], profit[c]/weight[c]) for c in range(len(picked_id))], key=lambda x: x[1])
    # print(ratio)
    while ind.vio:
        id = ratio[0][0]
        ind.kp[id-1] = 0
        violate(info, ind)
        ratio = ratio[1:]
    # print(ind.kp)
    # print(ind.weight, prob.W)
    # print()


def eva(info, ids_in_cities, ind):
    profit = 0
    weight = 0
    time = 0
    v = (info.max_speed - info.min_speed) / info.W
    for index in range(len(ind.tour)-1):
        this_city = ind.tour[index]
        next_city = ind.tour[index+1]
        # print(this_city, next_city)
        distance = info.dist[this_city][next_city]
        items = ids_in_cities[this_city]
        for item_id in items:
            if ind.kp[item_id-1] == 1:
                profit += info.profit[item_id - 1]
                weight += info.weight[item_id - 1]
        time += distance / (info.max_speed - (v * weight))

    distance = info.dist[ind.tour[-1]][0]
    items = ids_in_cities[ind.tour[-1]]
    for item_id in items:
        if ind.kp[item_id - 1] == 1:
            profit += info.profit[item_id - 1]
            weight += info.weight[item_id - 1]
    time += distance / (info.max_speed - (v * weight))
    ind.profit = profit
    ind.time = time
    ind.fitness = profit - (info.R * time)


def evaluate(info, ids_in_cities, ind):
    violate(info, ind)
    if ind.violate:
        repair(info, ind)
    eva(info, ids_in_cities, ind)

def opt(tour_list):
    selected_points = sorted(random.sample(range(0, len(tour_list)), 2))
    # print(selected_points)
    new_list = tour_list[:selected_points[0]] + tour_list[selected_points[0]:selected_points[1]][::-1] + tour_list[selected_points[1]:]
    return new_list


def flip(kp, probability):
    new_kp = []
    for elem in kp:
        if random.random() < probability:
            new_kp.append((elem+1)%2)
        else:
            new_kp.append(elem)
    return new_kp


def mutate(ind, opt_rate, flip_rate):
    mu = False
    ran = random.random()
    if ran < opt_rate:
        mu = True
        tsp = ind.tour[1:]
        ind.tour = [0] + opt(tsp)
    if ran < flip_rate:
        mu = True
        kp = ind.kp
        ind.kp = flip(kp, 0.002)
    return ind, mu


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
    c1 = Individual(new_tsp1, new_kp1)
    c2 = Individual(new_tsp2, new_kp2)
    return c1, c2


def tour_length(tour, dist):
    length = 0
    for i in range(len(tour)):
        length += dist[tour[i - 1]][tour[i]]
    return length


def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
    return new_tour


def lk(tour, dist, tours, id):
    best_tour = tour[:]
    best_length = tour_length(best_tour, dist)
    improvement = True
    budget = len(tour)*2000
    # budget = 100
    while improvement and budget > 0:
        improvement = False
        for i in range(1, len(tour) - 1):  # 从1开始，跳过第一个城市
            for j in range(i + 1, len(tour)):
                new_tour = two_opt_swap(tour, i, j)
                new_length = tour_length(new_tour, dist)
                budget -= 1
                if new_length < best_length:
                    # print('更新')
                    # print(f'{id}->{new_length}')
                    # print(new_tour)
                    best_tour = new_tour[:]
                    best_length = new_length
                    improvement = True
        tour = best_tour[:]
    print(f'处理器{id}预算用完！')
    tours.put(best_tour)


def clk(info, pop_size):
    tours = mp.Queue()
    processes = []
    for id in range(pop_size):
        init_tour = [num - 1 for num in info.city_ID[1:]]
        random.shuffle(init_tour)
        init_tour = [0] + init_tour
        print(f'处理器-{id}开始：')
        # print(init_tour)
        p = mp.Process(target=lk, args=(init_tour, info.dist, tours, id + 1))
        processes.append(p)
        p.start()

    exits = []
    for p in processes:
        p.join()
        exits.append(p.exitcode)

    raw_routes = []
    while not tours.empty():
        opt = tours.get()
        index_init = 0
        while opt[index_init] != 0:
            index_init += 1
        if index_init != 0:
            opt = opt[index_init:] + opt[:index_init]
        raw_routes.append(opt)
        formal_tour = [num + 1 for num in opt]
        length = tour_length(opt, info.dist)
        # print("Optimized tour:", formal_tour)
        # print("Tour length:", length)
    return raw_routes


def non_dominated_sorting(population):
    """
    Perform non-dominated sorting on the population of Individual objects.

    Parameters:
    population (list): List of Individual objects.

    Returns:
    list: List of fronts, where each front is a list of indices corresponding to solutions in that front.
    """
    fronts = [[]]
    domination_counts = [0] * len(population)
    dominated_solutions = [[] for _ in range(len(population))]

    for p in range(len(population)):
        for q in range(len(population)):
            if (population[p].time < population[q].time and population[p].profit >= population[q].profit) or \
                    (population[p].time <= population[q].time and population[p].profit > population[q].profit):
                dominated_solutions[p].append(q)
            elif (population[q].time < population[p].time and population[q].profit >= population[p].profit) or \
                    (population[q].time <= population[p].time and population[q].profit > population[p].profit):
                domination_counts[p] += 1

        if domination_counts[p] == 0:
            fronts[0].append(p)

    i = 0
    while fronts[i]:
        next_front = []
        for p in fronts[i]:
            for q in dominated_solutions[p]:
                domination_counts[q] -= 1
                if domination_counts[q] == 0:
                    next_front.append(q)
        i += 1
        fronts.append(next_front)

    fronts.pop()  # Remove the last empty front
    return fronts


import numpy as np


def crowding_distance(front, population):
    """
    Calculate the crowding distance for each solution in a front.

    Parameters:
    front (list): List of indices of solutions in the front.
    population (list): List of Individual objects.

    Returns:
    list: Crowding distance for each solution in the front.
    """
    distances = [0] * len(front)
    num_objectives = 2  # We have two objectives: time and profit

    for m in range(num_objectives):
        if m == 0:
            # Sort by time
            sorted_front = sorted(front, key=lambda x: population[x].time)
        else:
            # Sort by profit
            sorted_front = sorted(front, key=lambda x: population[x].profit)

        distances[0] = distances[-1] = float('inf')

        for i in range(1, len(front) - 1):
            if m == 0:
                if population[sorted_front[-1]].time == population[sorted_front[0]].time:
                    distances[i] += 0
                else:
                    distances[i] += (population[sorted_front[i + 1]].time - population[sorted_front[i - 1]].time) / \
                                    (population[sorted_front[-1]].time - population[sorted_front[0]].time)
            else:
                if population[sorted_front[-1]].profit == population[sorted_front[0]].profit:
                    distances[i] += 0
                else:
                    distances[i] += (population[sorted_front[i + 1]].profit - population[sorted_front[i - 1]].profit) / \
                                    (population[sorted_front[-1]].profit - population[sorted_front[0]].profit)

    return distances


def selection(population, fronts, crowding_distances, num_individuals):
    new_population = []
    i = 0
    while len(new_population) + len(fronts[i]) <= num_individuals:
        for ind in fronts[i]:
            new_population.append(population[ind].copying())
        i += 1

    sorted_front = sorted(
        fronts[i],
        key=lambda x: crowding_distances[i][fronts[i].index(x)],
        reverse=True
    )

    for ind in sorted_front:
        if len(new_population) < num_individuals:
            new_population.append(population[ind].copying())
        else:
            break

    return new_population