class Ind:
    def __init__(self, tour, kp):
        self.tour = tour
        self.kp = kp
        self.vio = True
        # single-objective
        self.fitness = 999999999
        self.weight = 0
        # bi-objective
        self.profit = 0
        self.time = 0

    def copy(self):
        ind = Ind(self.tour, self.kp)
        ind.fitness = self.fitness
        ind.weight = self.weight
        ind.profit = self.profit
        ind.time = self.time
        ind.vio = self.vio
        return ind
