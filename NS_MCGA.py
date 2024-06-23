import tool
import MCGA
import random


def dominance_relation(inda, indb):
    time_a, profit_a = inda.time, inda.profit
    time_b, profit_b = indb.time, indb.profit

    if (time_a <= time_b and profit_a >= profit_b) and (time_a < time_b or profit_a > profit_b):
        return -1  # individual_a dominates individual_b
    elif (time_b <= time_a and profit_b >= profit_a) and (time_b < time_a or profit_b > profit_a):
        return 1  # individual_b dominates individual_a
    else:
        return 0  # neither dominates the other


def bi_tournament(inda, indb):
    result = dominance_relation(inda, indb)
    if result == -1:
        return inda
    elif result == 1:
        return indb
    else:
        return random.choice([inda, indb])


def run(max_gen, info):
    pop_size = 200
    num_elite = 12
    order_cross = 1
    n_point_cross = 1
    opt_mutate = 0.85
    flip_mutate = 0.825
    bests = []
    times = []
    profits = []

    pop, ids_in_cities = MCGA.regular_initialise(info, pop_size)

    for gen in range(max_gen):
        last_pop = pop
        offspring = []
        while len(offspring) < pop_size:
            can1 = random.sample(last_pop, 2)
            can2 = random.sample(last_pop, 2)
            p1 = bi_tournament(can1[0], can1[1])
            p2 = bi_tournament(can2[0], can2[1])
            c1, c2 = tool.crossover(p1, p2, order_cross, n_point_cross)
            tool.evaluate(info, ids_in_cities, c1)
            tool.evaluate(info, ids_in_cities, c2)
            c1, mu1 = tool.mutate(c1, opt_mutate, flip_mutate)
            c2, mu2 = tool.mutate(c2, opt_mutate, flip_mutate)
            if mu1:
                tool.evaluate(info, ids_in_cities, c1)
            if mu2:
                tool.evaluate(info, ids_in_cities, c2)
            offspring.append(c1)
            offspring.append(c2)
        new_pop = last_pop+offspring
        # [[index]]
        fronts = tool.non_dominated_sorting(new_pop)
        crowding_distances = []
        for front in fronts:
            distances = tool.crowding_distance(front, new_pop)
            crowding_distances.append(distances)
        pop = tool.selection(new_pop, fronts, crowding_distances, pop_size)
        best = max(pop, key=lambda x: x.fitness)
        bests.append(best.fitness)
        times.append(best.time)
        profits.append(best.profit)
        print('time', new_pop[fronts[0][0]].time, new_pop[fronts[0][-1]].time)
        print('profit', new_pop[fronts[0][0]].profit, new_pop[fronts[0][-1]].profit)
        print(gen, best.fitness, best.time, best.profit)

    return pop, bests, times, profits


