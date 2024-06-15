import random
import tool

def regular_initialise(info, pop_size):
    ids_in_cities = {}
    for city_id in info.city_ID:
        items = []
        for index in range(len(info.item_ID)):
            if city_id == info.belongto[index]:
                items.append(info.item_ID[index])
        ids_in_cities[city_id - 1] = items

    pop = []
    tour_model = [(city_id - 1) for city_id in info.city_ID[1:]]
    empty_kp = [0]*info.total_items
    while len(pop) < pop_size:
        another_list = tour_model[:]
        random.shuffle(another_list)
        tour = [0] + another_list
        kp = empty_kp[:]
        ind = tool.Individual(tour, kp)
        tool.evaluate(info, ids_in_cities, ind)
        pop.append(ind)
    return pop, ids_in_cities

def run(max_gen, info):
    pop_size = 200
    num_elite = 12
    order_cross = 1
    n_point_cross = 1
    opt_mutate = 0.35
    flip_mutate = 0.825
    bests = []

    pop, ids_in_cities = regular_initialise(info, pop_size)

    for generation in range(max_gen):
        last_pop = pop
        # first selection
        parents = tool.tournament(last_pop, pop_size)
        offspring = []
        i = 0
        j = 1
        while j < pop_size:
            p1 = parents[i]
            p2 = parents[j]
            i += 2
            j += 2
            # crossover
            c1, c2 = tool.crossover(p1, p2, order_cross, n_point_cross)
            # evaluate children
            tool.evaluate(info, ids_in_cities, c1)
            tool.evaluate(info, ids_in_cities, c2)
            offspring.append(c1)
            offspring.append(c2)
        big_pop = sorted(last_pop + offspring, key=lambda x:x.fitness, reverse=True)
        elites = [some_ind.copying() for some_ind in big_pop[:num_elite]]
        next_gen = tool.tournament(big_pop, (pop_size-num_elite))
        # mutate
        for ind in next_gen:
            ind, mu = tool.mutate(ind, opt_mutate, flip_mutate)
            if mu:
                tool.evaluate(info, ids_in_cities, ind)
        next_gen = elites + next_gen
        bests.append(max(next_gen, key=lambda x: x.fitness).fitness)
        print(generation, elites[0].fitness)
        pop = next_gen
    return pop, bests







if __name__ == '__main__':
    info = tool.read_ttp('/Users/zepeng/travel_thief/dataset/a280-ttp/a280_n279_bounded-strongly-corr_01.ttp')
    run(max_gen=1000, info=info)