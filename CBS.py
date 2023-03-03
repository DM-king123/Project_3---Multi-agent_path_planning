import queue
import networkx as nx


# 优先级队列
open_list = queue.PriorityQueue()


# 需要一个路径节点类来表示路径及其相关信息。
# 路径包括路径的解和代价，以及与其他路径的约束集
# 定义路径
class PathNode:
    def __init__(self, solution, constraints):
        self.solution = solution
        self.cost = 0
        for i in solution:
            self.cost += len(i)
        self.constraints = constraints

    def __str__(self):
        return f'Path({self.solution}, {self.cost}, {self.constraints})'


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
        print("path:", path)
    return paths


# 解决冲突
def solve_conflicts(node, constraint):
    # 将约束分给两个节点
    if len(constraint) == 4:
        constraint1 = node.constraints + [constraint[0], constraint[2], constraint[3]]
        constraint2 = node.constraints + [constraint[1], constraint[2], constraint[3]]
    else:
        constraint1 = node.constraints + [constraint[0], constraint[2], constraint[3]]
        constraint2 = node.constraints + [constraint[1], constraint[2], constraint[4]]
    # --这个新path怎么求是个问题,CSDN上说用A*，所以变成了新增加的约束（障碍物）怎么加到A*里面的问题
    path1 = []
    path2 = []
    # 新节点放入open_list
    node1 = PathNode(path1, constraint1)
    node2 = PathNode(path2, constraint2)
    open_list.put((node1.cost, node1))
    open_list.put((node2.cost, node2))


# 查找冲突
def find_conflicts(node):
    for i in range(len(node.paths)-1):
        for j in range(i+1, len(node.paths)):
            for k in range(min(len(node.paths[i]), len(node.paths[j]))):
                # 当两条路径在同一时刻被两个小车占领
                if node.paths[i][k] == node.paths[j][k]:
                    constraint = [i, j, k, node.paths[i][k]]
                    return constraint
                # 当两个小车交换位置
                elif k != 0 and node.paths[i][k] == node.paths[j][k-1] and node.paths[i][k-1] == node.paths[j][k]:
                    constraint = [i, j, k, node.paths[i][k], node.paths[j][k]]
                    return constraint
    return []


# 解决问题
def solve(problem):
    paths = create_initial_paths(problem)
    # 将初始节点加入open_list,以cost为键值
    node_ini = PathNode(paths, [])
    open_list.put((node_ini.cost, node_ini))

    while True:
        # 找到cost最小的节点
        cost, node = open_list.get()
        # 若无冲突则得到解，返回最小的cost
        constraint = find_conflicts(node)
        if not constraint:
            return cost
        # 否则解决冲突
        solve_conflicts(node, constraint)
