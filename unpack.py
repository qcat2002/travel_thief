import csv
from data import Problem
import math

debug = False

def run(path):
    with open(path, 'r') as f:
        reader = csv.reader(f, delimiter='\t')
        problem = Problem.Problem()
        problem.name = next(reader)[1]
        problem.KP_type = next(reader)[0].split(': ')[1]
        problem.total_cities = int(next(reader)[1])
        problem.total_items = int(next(reader)[1])
        problem.W = int(next(reader)[1])
        problem.min_speed = float(next(reader)[1])
        problem.max_speed = float(next(reader)[1])
        problem.R = float(next(reader)[1])

        next(reader)
        next(reader)

        for _ in range(problem.total_cities):
            city = [float(number) for number in next(reader)]
            problem.city_ID.append(int(city[0]))
            problem.X.append(city[1])
            problem.Y.append(city[2])

        next(reader)

        for _ in range(problem.total_items):
            item = [int(number) for number in next(reader)]
            problem.item_ID.append(item[0])
            problem.profit.append(item[1])
            problem.weight.append(item[2])
            problem.belongto.append(item[3])

        problem.dist = [([0.00]*problem.total_cities) for _ in range(problem.total_cities)]
        if debug:
            for row in range(problem.total_cities):
                for col in range(problem.total_cities):
                    problem.dist[row][col] = ([row+1, col+1], math.sqrt((problem.X[row] - problem.X[col])**2 + (problem.Y[row] - problem.Y[col])**2))
        else:
            for row in range(problem.total_cities):
                for col in range(problem.total_cities):
                    problem.dist[row][col] = math.sqrt((problem.X[row] - problem.X[col]) ** 2 + (problem.Y[row] - problem.Y[col]) ** 2)
            # problem.info()
        if debug:
            problem.info()

        return problem


if __name__ == '__main__':
    # debug = True
    pro = run('/Users/zepeng/Git/new_TTP/data/dataset/a280-ttp/a280_n2790_bounded-strongly-corr_01.ttp')
