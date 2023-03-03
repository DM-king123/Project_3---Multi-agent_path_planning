import heapq


# 定义状态节点类
class Node:
    def __init__(self, x, y, t):
        self.x = x
        self.y = y
        self.t = t
        self.parent = None
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.t == other.t

    def __lt__(self, other):
        return self.f < other.f


# 定义地图类
class Map:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = [[1 for _ in range(width)] for _ in range(height)]

    # 判断节点是否在地图内，进行边界碰撞检测
    def is_valid(self, node):
        return 0 <= node.x < self.width and 0 <= node.y < self.height

    # 判断节点是否是障碍物，对于运动障碍物此处可添加其轨迹函数，每次调用实现实时判定
    def is_obstacle(self, node):
        return self.grid[node.y][node.x] == 1

    # 增加障碍物
    def add_obstacle(self, x, y):
        self.grid[y][x] = 1

    # 删除障碍物
    def remove_obstacle(self, x, y):
        self.grid[y][x] = 0

    # 计算节点之间的代价
    def cost(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    # 计算从起点到终点的启发式距离（使用 Manhattan 距离）
    def heuristic(self, a, b):
        return abs(a.x - b.x) + abs(a.y - b.y)

    # A*算法
    def astar(self, i_robot, start, goal, constraints):
        print("astar!")
        # 初始化开启列表和关闭列表，使用列表形式维护节点的状态改变
        open_list = []
        closed_list = []

        # 将起始状态节点加入开启列表
        heapq.heappush(open_list, start)

        # 循环查找路径
        while len(open_list) > 0:
            print("astar loop")
            # 选择估价函数 f(n) 值最小的状态节点 n
            current_node = heapq.heappop(open_list)

            # 如果节点 n 是目标状态节点，则返回路径
            if current_node.x == goal.x and current_node.y == goal.y:
                path = []
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent
                return path[::-1]
            goal.t += 1

            # 将节点 n 移入关闭列表中，并且考虑扩展它的邻居节点，这里可以使用方向价值函数为路径搜索剪枝，但是时间有限，我们暂时不会这么做
            closed_list.append(current_node)

            # 扩展当前节点的邻居节点
            for dx, dy, dt in [(0, -1, 1), (0, 1, 1), (-1, 0, 1), (1, 0, 1), (0, 0, 1)]:
                next_node = Node(current_node.x + dx, current_node.y + dy, current_node.t + dt)
                for constraint in constraints:
                    if constraint[1] == next_node.t and constraint[0] == i_robot:
                        self.add_obstacle(constraint[2][0], constraint[2][1])
                    else:
                        self.remove_obstacle(constraint[2][0], constraint[2][1])
                if not self.is_valid(next_node) or self.is_obstacle(next_node):
                    continue

                # 计算从起始节点到节点的代价函数
                cost = self.cost(current_node, next_node)
                next_node_g = current_node.g + cost

                # 如果节点已经在关闭列表中，则跳过
                if next_node in closed_list:
                    continue

                # 如果节点已经在开启列表中，更新 g 值和父节点
                if next_node in open_list:
                    idx = open_list.index(next_node)
                    next_node = open_list[idx]
                    if next_node_g < next_node.g:
                        next_node.g = next_node_g
                        next_node.f = next_node.g + next_node.h
                        next_node.parent = current_node

                # 如果节点不在开启列表中，则加入开启列表
                else:
                    next_node.g = next_node_g
                    next_node.h = self.heuristic(next_node, goal)
                    next_node.f = next_node.g + next_node.h
                    next_node.parent = current_node
                    heapq.heappush(open_list, next_node)

        # 如果找不到路径，返回空列表
        return []


