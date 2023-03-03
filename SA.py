import math
import copy
import random
import pandas as pd
import numpy as np
import CBS


# urban model
# 城市模型类
# 包括机器人和任务的数量，每个节点的需求，每个小车的运载量和每个节点的位置
# 这里读入csv文件，需求量不为0的点默认为每个任务点
class Model:
    def __init__(self):
        # model parameters
        self.robot_num = 0
        self.task_num = 0
        self.need = list()
        self.supply = list()
        self.positions = list()

        # read region parameters
        filename = 'parameter/node.csv'
        data = pd.read_csv(filename, usecols=[2, 3, 4])
        data_list = data.values.tolist()
        for i in data_list:
            if i[0] == 0:
                continue
            self.need.append((i[0]))
            self.positions.append((i[1], i[2]))

        # model parameters
        self.robot_num = len(self.need)
        self.task_num = self.robot_num
        # --这里supply我暂时把所有小车都定为1000了，到时候可以改变一下
        self.supply = [1000] * self.robot_num


# 定义问题
# 我们需要让40个运输车到达指定的目的地。
# 可以将每个车辆表示为一个独立的实体，并使用它们的起点和目的地作为问题的输入。
# 还需要将地图划分为一个个网格，并使用网格坐标来表示每个车辆的位置。
# 可以使用numpy库来处理网格坐标。
class Problem:
    def __init__(self, start_positions, goal_positions, grid_size):
        self.start_positions = np.array(start_positions)
        self.goal_positions = np.array(goal_positions)
        self.grid_size = grid_size


# Termination temperature
Te = 0.01
# Annealing rate
k = 0.99
# urban model
M = Model()
# iterations
iterations = 300

grid_size = 20
# --这里开始节点应该还要重新改改，应该用医院的位置比较好
problem = Problem(M.positions, M.positions, grid_size)


# Randomly generate new solutions
def new_solution(strategy_origin):
    i = random.randint(1, M.task_num - 2)
    j = random.randint(i + 1, M.task_num - 1)
    # Choose a method to generate the new solution
    func = random.randint(0, 3)
    strategy_new = copy.deepcopy(strategy_origin)

    while True:
        if func == 0:
            # Switch tasks between two robots
            strategy_new[i], strategy_new[j] = strategy_new[j], strategy_new[i]
        elif func == 1:
            # Flip a length of task allocation
            strategy_new[i:j] = list(reversed(strategy_new[i:j]))
        elif func == 2:
            # Shift the assignment to the left
            strategy_new = strategy_new[i:j] + strategy_new[:i] + strategy_new[j:]
        else:
            # Flip both ends of task allocation
            strategy_new[:i] = list(reversed(strategy_new[:i]))
            strategy_new[j:] = list(reversed(strategy_new[j:]))
        if is_legal(strategy_new):
            break
    positions_new = list()
    for i in strategy_new:
        positions_new.append(M.positions[i])
    problem_new = Problem(M.positions, positions_new, grid_size)
    cost_new = CBS.solve(problem_new)
    return strategy_new, cost_new


# whether the new strategy is legal
# 默认小车和任务是双射的关系，所以用需求和每个小车的supply比较判断
def is_legal(strategy):
    i = 0
    for j in strategy:
        if M.need[j] > M.supply[i]:
            return False
        i += 1
    return True


# Simulate Anealing
def SA():
    # Initial temperature
    Ti = 5000
    # Initial task allocation strategy and temperature
    strategy = list(range(M.task_num))
    cost = CBS.solve(problem)

    # While the termination temperature was not reached
    while Ti > Te:
        # Generate new solution
        for i in range(iterations):
            strategy_new, cost_new = new_solution(strategy)

            # Accept the new solution according to the probability formula
            if cost_new <= cost or math.exp(-(cost_new - cost) / Ti) > random.random():
                strategy = strategy_new
                cost = cost_new

        # Lower the temperature
        Ti *= k

        # Print the final task allocation strategy
        for i in range(len(strategy)):
            print("Robot ", i, " : task ", strategy[i])


if __name__ == "__main__":
    print('Runing......')
    SA()
    print('Succeed!')
