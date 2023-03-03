import numpy as np
import networkx as nx
# 定义问题
#我们需要让40个运输车到达指定的目的地。
# 可以将每个车辆表示为一个独立的实体，并使用它们的起点和目的地作为问题的输入。
# 还需要将地图划分为一个个网格，并使用网格坐标来表示每个车辆的位置。
# 可以使用numpy库来处理网格坐标。
class Problem:
    def __init__(self, start_positions, goal_positions, grid_size):
        self.start_positions = np.array(start_positions)
        self.goal_positions = np.array(goal_positions)
        self.grid_size = grid_size


# 创建初始路径
# 对于每个运输车，使用A算法计算从其起点到目的地的最短路径。
# 这将是我们的初始路径。
def create_initial_paths(problem):
    paths = []
    for i in range(len(problem.start_positions)):
        start = tuple(problem.start_positions[i])
        goal = tuple(problem.goal_positions[i])
        g = nx.grid_graph(dim=[problem.grid_size]*2)
        path = nx.astar_path(g, start, goal)
        paths.append(path)
    return paths

# 需要一个路径类来表示路径及其相关信息。
# 路径包括路径的起点、终点和代价，以及与其他路径的约束集
# 定义路径
class Path:
    def __init__(self, start, goal, cost, constraints=[]):
        self.start = start
        self.goal = goal
        self.cost = cost
        self.constraints = constraints

    def __str__(self):
        return f'Path({self.start}, {self.goal}, {self.cost}, {self.constraints})'

# 需要一个约束集类来表示路径的约束集。每个约束集包含多个路径，这些路径不能同时出现在同一位置。
# 定义约束集
class ConstraintSet:
    def __init__(self, paths=[]):
        self.paths = paths

    def add_path(self, path):
        self.paths.append(path)

    def remove_path(self, path):
        self.paths.remove(path)

    def __str__(self):
        return f'ConstraintSet({len(self.paths)} paths)'

# 需要一个冲突检测函数来检测两个路径是否在某个位置发生冲突。
# 冲突检测
def check_conflict(path1, path2):
    for i in range(len(path1)):
        if path1[i] == path2[i]:
            return True
    return False

# 使用CBS算法来解决路径之间的冲突。
# 我们从初始路径开始，将每个路径都分配到一个独立的代理，以便我们可以在路径之间找到冲突，并通过合并路径来解决冲突。
# 解决冲突
def solve_conflicts(problem, paths):
    constraints = ConstraintSet()
    for i in range(len(paths)):
        constraints.add_path(Path(paths[i][0], paths[i][-1], len(paths[i])-1))
    while True:
        conflict_paths = find_conflicts(constraints)
        if not conflict_paths:
            break
        merge_paths(problem, constraints, conflict_paths)
    return constraints

# 查找冲突
def find_conflicts(constraints):
    conflict_paths = []
    for i in range(len(constraints.paths)):
        for j in range(i+1, len(constraints.paths)):
            if check_conflict(constraints.paths[i].start, constraints.paths[j].start) or \
                check_conflict(constraints.paths[i].goal, constraints.paths[j].goal):
                conflict_paths.append((i, j))
    return conflict_paths

# 合并路径
def merge_paths(problem, constraints, conflict_paths):
    for (i, j) in conflict_paths:
        merged_path = merge(problem, constraints.paths[i], constraints.paths[j])
        constraints.remove_path(constraints.paths[i])
        constraints.remove_path(constraints.paths[j-1])
        constraints.add_path(merged_path)

# 合并路径
def merge(problem, path1, path2):
    merged_path = Path(path1.start, path2.goal, path1.cost+path2.cost, path1.constraints+path2.constraints)
    return merged_path

# 解决问题
def solve(problem):
    paths = create_initial_paths(problem)
    constraints = solve_conflicts(problem, paths)
    return constraints

# 示例问题
start_positions = [(0,0), (0,10), (10,0), (10,10)] * 10
goal_positions = [(10,10), (10,0), (0,10), (0,0)] * 10
grid_size = 20
problem = Problem(start_positions, goal_positions, grid_size)

# 解决问题并打印结果
constraints = solve(problem)
print(constraints)

