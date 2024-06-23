import tool
import MCGA


def run(max_gen, info):
    pop_size = 200
    num_elite = 12
    order_cross = 1
    n_point_cross = 1
    opt_mutate = 0.35
    flip_mutate = 0.825
    bests = []
    times = []
    profits = []

    abc, ids_in_cities = MCGA.regular_initialise(info, pop_size)
    pop = []
    empty_kp = [0] * info.total_items
    remain = pop_size
    while remain > 0:
        consume = remain
        if remain >= 10:
            consume = 10
        remain -= consume
        raw_routes = tool.clk(info, consume)
        for index in range(len(raw_routes)):
            ind = tool.Individual(raw_routes[index], empty_kp[:])
            tool.evaluate(info, ids_in_cities, ind)
            pop.append(ind)

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
        big_pop = sorted(last_pop + offspring, key=lambda x: x.fitness, reverse=True)
        elites = [some_ind.copying() for some_ind in big_pop[:num_elite]]
        next_gen = tool.tournament(big_pop, (pop_size - num_elite))
        # mutate
        for ind in next_gen:
            ind, mu = tool.mutate(ind, opt_mutate, flip_mutate)
            if mu:
                tool.evaluate(info, ids_in_cities, ind)
        next_gen = elites + next_gen
        best = max(next_gen, key=lambda x: x.fitness)
        bests.append(best.fitness)
        times.append(best.time)
        profits.append(best.profit)
        print(generation, elites[0].fitness)
        pop = next_gen
    return pop, bests, times, profits
