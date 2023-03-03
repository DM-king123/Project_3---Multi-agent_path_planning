###### 第一部分：导入必要的库和定义类
import random
import math

# 定义问题类
class Problem:
    def __init__(self, start_nodes, goal_nodes, edges):
        self.start_nodes = start_nodes
        self.goal_nodes = goal_nodes
        self.edges = edges

# 定义路径类
class Path:
    def __init__(self, start_node, goal_node, length, nodes=None):
        self.start_node = start_node
        self.goal_node = goal_node
        self.length = length
        self.nodes = nodes if nodes else []

    def __str__(self):
        return "Path from {} to {}: {}".format(self.start_node, self.goal_node, self.nodes)

# 定义约束类
class Constraints:
    def __init__(self, paths, node_constraints):
        self.paths = paths
        self.node_constraints = node_constraints

    def __str__(self):
        return "Paths: {}\nNode constraints: {}".format(self.paths, self.node_constraints)

###### 第二部分：计算成本函数
# 计算成本函数
def compute_cost(problem, paths):
    cost = 0
    # 对于每条路径
    for path in paths:
        # 添加路径长度
        cost += path.length
        # 添加从起点到第一个节点的代价
        if path.start_node in problem.start_nodes:
            cost += problem.start_nodes[path.start_node]
        # 添加从最后一个节点到终点的代价
        if path.goal_node in problem.goal_nodes:
            cost += problem.goal_nodes[path.goal_node]
        # 添加路径中的边的代价
        for i in range(len(path.nodes) - 1):
            edge = (path.nodes[i], path.nodes[i+1])
            if edge in problem.edges:
                cost += problem.edges[edge]
            elif (edge[1], edge[0]) in problem.edges:
                cost += problem.edges[(edge[1], edge[0])]
            else:
                raise ValueError("Edge not found: {}".format(edge))
    return cost

###### 第三部分：路径优化函数
# 对单个路径进行优化
def optimize_path(problem, constraints, path, temperature):
    current_path = [node for node in path.nodes]
    current_cost = compute_cost(problem, [path])
    while True:
        new_path = perturb_path(problem, constraints, current_path)
        new_cost = compute_cost(problem, [Path(new_path[0], new_path[-1], len(new_path)-1)])
        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temperature):
            current_path = new_path
            current_cost = new_cost
        else:
            break
    return Path(current_path[0], current_path[-1], len(current_path)-1)

###### 第四部分：路径扰动函数
# 路径扰动函数
def perturb_paths(problem, constraints, paths):
    perturbed_paths = []
    for path in paths:
        if len(path.nodes) < 3:
            perturbed_paths.append(path)
        else:
            # 插入随机节点
            perturbed_path = insert_random_node(problem, constraints, path)
            # 删除随机节点
            perturbed_path = delete_random_node(problem, constraints, perturbed_path)
            # 交换随机节点
            perturbed_path = swap_random_nodes(problem, constraints, perturbed_path)
            perturbed_paths.append(Path(perturbed_path))
    return perturbed_paths

# 插入随机节点
def insert_random_node(problem, constraints, path):
    perturbed_path = [path.start_node]
    for i in range(1, len(path.nodes)):
        node = path.nodes[i]
        perturbed_path.append(node)
        # 以一定的概率插入随机节点
        if random.uniform(0, 1) < 0.2:
            # 获取可以插入的节点
            available_nodes = [n for n in problem.nodes if n not in perturbed_path and n not in constraints.node_constraints]
            if len(available_nodes) > 0:
                # 插入随机节点
                new_node = random.choice(available_nodes)
                perturbed_path.append(new_node)
    perturbed_path.append(path.goal_node)
    return perturbed_path

# 删除随机节点
def delete_random_node(problem, constraints, path):
    perturbed_path = [path.start_node]
    for i in range(1, len(path.nodes) - 1):
        node = path.nodes[i]
        # 以一定的概率删除节点
        if random.uniform(0, 1) < 0.2 and node not in constraints.node_constraints:
            continue
        perturbed_path.append(node)
    perturbed_path.append(path.goal_node)
    return perturbed_path

# 交换随机节点
def swap_random_nodes(problem, constraints, path):
    perturbed_path = [path.start_node]
    for i in range(1, len(path.nodes) - 1):
        node = path.nodes[i]
        # 以一定的概率交换节点
        if random.uniform(0, 1) < 0.2 and node not in constraints.node_constraints:
            available_nodes = [n for n in problem.nodes if n not in perturbed_path and n not in constraints.node_constraints]
            if len(available_nodes) > 0:
                new_node = random.choice(available_nodes)
                perturbed_path.append(new_node)
            else:
                perturbed_path.append(node)
        else:
            perturbed_path.append(node)
    perturbed_path.append(path.goal_node)
    return perturbed_path

###### 第五部分：模拟退火算法
# 模拟退火算法
def simulated_annealing(problem, constraints, initial_paths, initial_temperature, cooling_rate, max_iterations):
    current_paths = initial_paths
    current_cost = compute_cost(problem, current_paths)
    temperature = initial_temperature
    for i in range(max_iterations):
        # 优化所有路径
        new_paths = []
        for path in current_paths:
            new_path = optimize_path(problem, constraints, path, temperature)
            new_paths.append(new_path)
        # 检查路径是否满足约束
        for path in new_paths:
            if path.start_node in constraints.node_constraints or path.goal_node in constraints.node_constraints:
                raise ValueError("Start/goal node in constraints: {}".format(path))
            for i in range(len(path.nodes) - 1):
                edge = (path.nodes[i], path.nodes[i+1])
                if edge in constraints.paths:
                    raise ValueError("Edge in constraints: {}".format(edge))
        # 计算新的成本
        new_cost = compute_cost(problem, new_paths)
        # 接受新的状态
        if new_cost < current_cost or random.uniform(0, 1) < math.exp((current_cost - new_cost) / temperature):
            current_paths = new_paths
            current_cost = new_cost
        # 降温
        temperature *= cooling_rate
    return current_paths, current_cost
