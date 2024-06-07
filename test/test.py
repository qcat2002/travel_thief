import clk
import random

def testing(problem):
    initial = [num-1 for num in problem.city_ID[1:]]
    random.shuffle(initial)
    initial = [0] + initial
    print(initial)
    # return initial, 100
    opt = clk.LK(initial, problem.dist)

    index_ini = 0
    while opt[index_ini] != 0:
        index_ini += 1

    if index_ini != 0:
        opt = opt[index_ini:] + opt[:index_ini]

    temp = [num+1 for num in opt]
    length = clk.tour_length(opt, problem.dist)
    print("Optimized tour:", temp)
    print("Tour length:", length)
    return opt, length
