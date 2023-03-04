# Project_3---Multi-agent_path_planning
Multi-agent path planning algorithm
## 项目介绍：本实验是我们小组跟随剑桥大学Amanda教授进行的的线上项目，以“移动机器人”为题自主发散构建的任务。
*  它有以下几个特点：
    *  我们以疫情期间的高校为任务背景，使用webots平台搭建了1：1大小的仿真环境，以期模拟现实中药品物资在一个封闭环境中的供求关系。
    *  对于仿真环境。我们使用抽象自“山东建筑大学”实际校园环境中的“道路”作为主要数据来源和参照构建城市模型。我们微缩了更多的城市景观（如居民楼，商业综合体等）放入仿真环境，以期得到更大的需求量参数和复杂的任务环境）
    *  对于城市规划。我们使用道路的交叉节点作为某个周边区域包含的所有建筑的“资源中转站”，以期简化和明确机器人的任务。
    *  对于机器人模型构建。在有限的任务时间内我们构建了一个简单的无人小车，它包含一个GPS传感器（用于自身定位）；一个惯性单元（检测自己是否偏航）；一个距离传感器（与周边环境进行碰撞检测）；一组信号的接收发送单元（用于与中心计算节点的通信）
    *  对于算法体系的设计。我们分解了任务要求，使用（A*+CBS）+SA的方式完成了多智能体任务及路径规划的需需要，有关算法和代码的详细介绍与说明将在下面的部分给出。
    *  对于项目中算法的进行流程。使用（A*+CBS）+SA算法体系的中心计算节点会向全局机器人发送任务说明，包括任务路径及执行时间。机器人通过信息的首发单元完成有关任务。
* 需要特别声明的是，本项目在环境设计和算法构思上还不完善，为了更好的效率和更优秀的可视化，本代码库也会持续更新。

## 多智能体路径规划算法设计：
* 1.我们可以将问题建模为集中式冲突有向无环图（DC-DAG），其中节点表示机器人执行任务的状态，边表示两个状态之间的转换（例如，机器人从一个位置移动到另一个位置）。
* 2.初始化初始状态。初始状态可以是所有机器人都在其起始位置，并且没有任何任务被分配的状态，我们设计了三家“医院”作为机器人的初始位置。
* 3.通过模拟退火算法搜索解空间。在模拟退火过程中，通过对机器人路径进行调整的方法来产生新状态，并根据一定概率接受这些新状态。随着搜索的进行，温度逐渐降低，概率接受次优解的可能性逐渐降低。
* 4.对于每个生成的状态，使用CBS算法进行路径规划。CBS算法是一种针对多智能体路径规划问题的启发式搜索算法，可在存在冲突的情况下为每个机器人找到最短路径。在每个状态下，使用CBS算法计算出机器人路径。
* 5.根据CBS算法得到的机器人路径，计算出每个状态的代价。通过比较代价，选择最佳状态。
* 6.重复步骤3-5直到达到停止条件（例如达到最大迭代次数或找到可接受的解）。
* 7.返回最佳状态下的任务分配和路径规划结果。

### 算法设计难点：
1. 在模拟退火算法中，需要设计合适的邻域结构，即如何生成新的状态。可以考虑交换机器人的任务分配或微调机器人的路径等操作。
2. 在CBS算法中，需要考虑如何处理机器人之间的冲突。一种常用的方法是在路径规划中添加冲突检测模块，当检测到冲突时，采取一些策略进行冲突解决，例如重规划、等待或者协调。
3. 在模拟退火算法中，需要设置合适的温度下降策略，以控制搜索过程的渐进性和可接受解的可能性。一种常用的策略是指数衰减，即随着搜索的进行，温度按指数函数逐渐降低。
4. 在计算代价时，可以设置不同的权重来平衡任务完成时间和机器人移动距离的影响。可以根据具体问题的要求进行调整。
5. 在最终结果中，需要对机器人的路径进行优化，例如通过平滑路径来减少机器人的转弯和减小路径长度。
6. 我们将依次介绍整个算法流程中A*算法，CBS算法和SA算法的设计与核心语句。

* 算法设计流程图
![mmexport1677833311483](https://user-images.githubusercontent.com/109540164/222877814-545c6105-70e5-439e-906d-bdb26903af3f.jpg)
## 一、基于平面地图和时间维度的 A* 算法设计——用于生成任务路径

### 算法流程设计：
1. 定义状态节点：我们定义一个节点表示机器人在地图上的位置和时间状态。节点可以表示为 (x, y, t)，其中 (x, y) 是机器人在平面地图上的坐标，t 是机器人在时刻 t 的状态。
2. 定义状态转移函数：我们需要定义一个函数来计算从一个状态节点到另一个状态节点的成本。假设两个状态节点分别为 n1=(x1, y1, t1) 和 n2=(x2, y2, t2)，则状态转移函数可以表示为：
cost(n1, n2) = euclidean_distance(n1, n2) + time_diff(n1, n2)
其中 euclidean_distance(n1, n2) 表示从 n1 到 n2 的欧几里得距离， time_diff(n1, n2) 表示从 n1 到 n2 的时间差。
3. 定义启发式函数：我们需要定义一个启发式函数来估计从当前状态节点到目标状态节点的最短距离。可以使用启发式函数来加速算法，以便它可以更快地找到解决方案。假设当前状态节点为 n=(x, y, t)，目标状态节点为 goal=(x_goal, y_goal, t_goal)，则启发式函数可以表示为：
h(n) = euclidean_distance(n, goal) + time_diff(n, goal)
其中 euclidean_distance(n, goal) 表示从当前状态节点 n 到目标状态节点 goal 的欧几里得距离， time_diff(n, goal) 表示从当前状态节点 n 到目标状态节点 goal 的时间差。
4. 运行 A* 算法：使用上述状态节点、状态转移函数和启发式函数，可以运行 A* 算法来搜索最短路径。具体步骤如下：
    * 初始化起始状态节点和目标状态节点。
    * 将起始状态节点加入到开启列表中，并将其 f(n) 值设置为启发式函数值 h(n)。
    * 重复以下步骤，直到找到解决方案或者开启列表为空：
    * 从开启列表中选择估价函数 f(n) 值最小的状态节点 n。
    * 如果节点 n 是目标状态节点，则返回路径。
    * 将节点 n 移入关闭列表中，并且考虑扩展它的邻居节点。
    * 对于每个邻居节点 m，计算从起始节点到节点 m 的实际成本 ：
                g(m) = g(n) + cost(n, m)
    * 如果节点 m 已经在开启列表中，并且当前的 g(m) 值小于之前的值，则更新节点 m 的 g(m) 值，并将其父节点设置为 n。
    * 如果节点 m 不在开启列表中，则将节点 m 加入开启列表中，并设置 g(m) 为当前计算出的值，并将其父节点设置为 n，同时将其 f(m) 值设置为 g(m) + h(m)。
    * 如果开启列表为空，则表示无解。

在 A* 算法中，估价函数 f(n) 值可以表示为：
f(n) = g(n) + h(n)
其中，g(n) 表示从起始节点到节点 n 的实际成本，h(n) 表示从节点 n 到目标节点的启发式估计成本。算法的目标是找到最小的 f(n) 值，这意味着它正在尝试找到一条最短路径。在算法执行过程中，开启列表和关闭列表可以使用堆或哈希表来优化搜索速度，这样在保留A*算法进行路径规划计算速度同时，可以优化由于开启列表和关闭列表时遍历操作带来的时间成本。



## 二、基于CBS算法的路径冲突检测。

### 算法流程设计：
0. 导入必要的模块。包括使用queue库设计创建一个优先级队列 open_list 用于存储待扩展的路径节点。
            open_list = queue.PriorityQueue()
1. 定义一个类 PathNode 用于表示路径及其相关信息。PathNode 类包含了路径的解和代价，以及与其他路径的约束集。
2. 定义create_initial_paths函数，它使用A*算法来计算每个运输车的初始路径，将所有初始路径存储在一个列表中，并返回该列表。.
3. 定义find_conflicts函数，它用于查找路径中的冲突。具体地，它通过遍历每对路径上的节点，来检查它们是否存在交叉和重叠情况，如果有，则返回相应的约束。
4. 定义了solve_conflicts函数，它用于解决路径冲突。具体地，它将约束分配给两个新的路径节点，并将这两个节点插入到优先级队列中。
5. 定义了solve函数，它是整个程序的主要函数。它首先使用create_initial_paths函数计算出初始路径，并将初始节点加入到优先级队列中。然后进入一个循环，直到找到无冲突的解为止。在每次迭代中，它找到当前cost最小的节点，然后调用find_conflicts函数来查找路径冲突。如果没有冲突，则返回最小cost值作为解。否则，它会调用solve_conflicts函数来解决冲突。
* 程序经以上流程得到最终的解，即为每个运输车的路径。
### CBS算法设计细节：
1. 初始化 
  a. 根据问题定义初始状态，包括：网格地图，包括大小、障碍物位置、起点和目标点位置等；运输车辆的起点和目标点位置； 
  b. 将初始状态存储在问题定义的数据结构中； 
  c. 创建一个优先级队列open_list，并将初始状态加入队列。
2. 搜索 
  * a. 从open_list中选取当前代价最小的路径节点，作为当前搜索节点； 
  * b. 检查当前搜索节点是否满足所有约束条件，若满足，则返回当前搜索节点的代价，算法结束； 
  * c. 如果当前搜索节点存在冲突，则解决冲突，具体步骤如下：
    * 找到冲突（Conflict）；
    * 将冲突分解为两个约束条件（Constraint）；
    * 根据约束条件创建两个新的路径节点，并将它们加入open_list中；
    * 重复步骤2，直到找到一个满足所有约束条件的节点或open_list为空。
 3. 解决冲突 
  * a.找到冲突：
    * 冲突类型一：两个运输车在同一时间占用同一个位置；
    * 冲突类型二：两个运输车在交叉位置交换位置。
  * b. 分解冲突为两个约束条件：
    * 约束条件一：阻止第一个运输车通过冲突位置；
    * 约束条件二：阻止第二个运输车通过冲突位置。 
  * c. 创建两个新的路径节点：
    * 新路径节点一：修改第一个运输车的路径，使其避开冲突位置；
    * 新路径节点二：修改第二个运输车的路径，使其避开冲突位置。 
  * d. 将两个新的路径节点加入open_list中。
4. 输出解 
  * a. 当找到一个满足所有约束条件的路径节点时，将该节点的代价作为最终解输出； 	
  * b. 如果open_list为空，算法无法找到满足所有约束条件的路径，输出无解。



## 三、基于模拟退火算法的任务优化
* 为了算法输出的合理性，我们实现了一个使用模拟退火算法（SA）优化任务分配的部分，用以在解空间中搜索一个全局最优解。在这里，SA算法被用来接续CBS算法的工作，搜索最优的任务分配策略，使得所有的任务都能被完成，同时最小化总的执行代价。
### 算法流程设计：
* 定义了一个城市模型类，包括机器人和任务的数量，每个节点的需求，每个小车的运载量和每个节点的位置。
* 定义了一个问题类，将地图划分为一个个网格，并使用网格坐标来表示每个车辆的位置。	使用CBS算法求解当前任务分配策略的总代价，并根据一定的概率来接受或者拒绝新的策略。
* 输出最终的任务分配策略。
#### 该算法的主要思想如下：
* 在一个初始温度下随机生成一个初始的任务分配策略
* 然后对于这个初始策略不断地生成新的策略，并根据一定的概率来接受或者拒绝这个新的策略。
* 在这个过程中，温度逐渐降低，概率逐渐变得更加严格，最终达到一个稳定的最优解。
```python
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
            
```
      
* 另外的，代码库中我们上传了实验过程中解决同一问题的不同方法，希望能够为访问者提供更多收获。
* 特别的，库中有road_pic2matrix.py文件，完成了一个视觉任务，将一个有灰色道路和白色背景的图片数据（库中road.png文件是其测试数据）按照像素切割识别出来，数值化后形成01矩阵，以便将地图数据输入算法。很有趣，所以一并放入项目中。
