def LK(tour, dist):
    best_tour = tour[:]
    best_length = tour_length(best_tour, dist)
    improvement = True
    budget = 0
    while improvement:
        improvement = False
        for i in range(1, len(tour) - 1):  # 从1开始，跳过第一个城市
            for j in range(i + 1, len(tour)):
                new_tour = two_opt_swap(tour, i, j)
                new_length = tour_length(new_tour, dist)
                budget += 1
                if new_length < best_length:
                    # print('更新')
                    print(new_length, best_length)
                    # print(new_tour)
                    best_tour = new_tour[:]
                    best_length = new_length
                    improvement = True
        tour = best_tour[:]
        # print(budget)
    return best_tour


def two_opt_swap(tour, i, j):
    new_tour = tour[:i] + tour[i:j+1][::-1] + tour[j+1:]
    return new_tour


def tour_length(tour, dist):
    length = 0
    for i in range(len(tour)):
        length += dist[tour[i - 1]][tour[i]]
    return length


def set_starting_point(tour, start_point):
    """Rearranges the tour to start from the specified start_point."""
    start_index = tour.index(start_point)
    return tour[start_index:] + tour[:start_index]


if __name__ == '__main__':
    # Example usage
    initial_tour = [0, 4, 3, 9, 5, 6, 1, 2, 7, 8]
    distance_matrix = [
        # Example distance matrix (fill with actual distances)
        [0, 29, 20, 21, 16, 31, 100, 12, 4, 31],
        [29, 0, 15, 29, 28, 40, 72, 21, 29, 41],
        [20, 15, 0, 15, 14, 25, 81, 9, 23, 27],
        [21, 29, 15, 0, 4, 12, 92, 12, 25, 13],
        [16, 28, 14, 4, 0, 16, 94, 9, 20, 16],
        [31, 40, 25, 12, 16, 0, 95, 24, 36, 3],
        [100, 72, 81, 92, 94, 95, 0, 90, 101, 99],
        [12, 21, 9, 12, 9, 24, 90, 0, 15, 25],
        [4, 29, 23, 25, 20, 36, 101, 15, 0, 35],
        [31, 41, 27, 13, 16, 3, 99, 25, 35, 0]
    ]
    # Specify the starting point
    start_point = 3
    initial_tour = set_starting_point(initial_tour, start_point)

    optimized_tour = LK(initial_tour, distance_matrix)

    index_ini = 0
    while optimized_tour[index_ini] != 0:
        index_ini += 1

    if index_ini != 0:
        optimized_tour = optimized_tour[index_ini:] + optimized_tour[:index_ini]

    print("Optimized tour:", optimized_tour)
    print("Tour length:", tour_length(optimized_tour, distance_matrix))