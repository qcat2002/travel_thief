# import matplotlib.pyplot as plt
# import test
# from data import unpack
#
# def run():
#     path = '/Users/zepeng/Git/new_TTP/data/dataset/a280-ttp/a280_n2790_bounded-strongly-corr_01.ttp'
#     problem = unpack.run(path)
#
#     for _ in range(1):
#         route, length = test.testing(problem)
#         plt.figure(figsize=(12, 11), dpi=400)
#         plt.scatter(problem.X, problem.Y)
#
#         for index in range(len(route)-1):
#             x1, x2 = problem.X[route[index]], problem.X[route[index+1]]
#             y1, y2 = problem.Y[route[index]], problem.Y[route[index+1]]
#             plt.plot([x1, x2], [y1, y2], color='red')
#
#         plt.title(f'Route-{length}', size=22, weight='bold')
#         plt.savefig(f'{_}-{length}.png')
#         plt.show()
#
# if __name__ == '__main__':
#     run()
