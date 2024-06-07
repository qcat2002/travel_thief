class Problem:
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

    def info(self):
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
        print('城市信息列表 (ID, X, Y)')
        for index in range(self.total_cities):
            print(f'ID: {self.city_ID[index]:<5} X: {self.X[index]:<8} Y: {self.Y[index]:<8}')
        print('==================================')
        print('物品信息列表 (ID, profit, weight, which city?)')
        for index in range(self.total_items):
            print(f'ID: {self.item_ID[index]:<5} profit: {self.profit[index]:<8} weight: {self.weight[index]:<8} city_ID:{self.belongto[index]:<5}')
        print('==================================')
        for row_elem in self.dist:
            chain = ''
            for col_elem in row_elem:
                chain += f'{str(col_elem):<35}'
            print(chain)
        print(len(self.dist), len(self.dist[0]))