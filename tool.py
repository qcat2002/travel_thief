import random
import csv
import math


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