# Project_3---Multi-agent_path_planning
Multi-agent path planning algorithm
## 项目说明 - 写在前面的话
### 项目介绍：本实验是我们小组跟随剑桥大学Amanda教授进行的的线上项目，以“移动机器人”为题自主发散构建的任务。
* 它有以下几个特点：
    1. 我们以疫情期间的高校为任务背景，使用webots平台搭建了1：1大小的仿真环境，以期模拟现实中药品物资在一个封闭环境中的供求关系。
    2. 对于仿真环境。我们使用抽象自“山东建筑大学”实际校园环境中的“道路”作为主要数据来源和参照构建城市模型。我们微缩了更多的城市景观（如居民楼，商业综合体等）放入仿真环境，以期得到更大的需求量参数和复杂的任务环境）
    3. 对于城市规划。我们使用道路的交叉节点作为某个周边区域包含的所有建筑的“资源中转站”，以期简化和明确机器人的任务。
    4. 对于机器人模型构建。在有限的任务时间内我们构建了一个简单的无人小车，它包含一个GPS传感器（用于自身定位）；一个惯性单元（检测自己是否偏航）；一个距离传感器（与周边环境进行碰撞检测）；一组信号的接收发送单元（用于与中心计算节点的通信）
    5. 对于算法体系的设计。我们分解了任务要求，使用（A*+CBS）+SA的方式完成了多智能体任务及路径规划的需需要，有关算法和代码的详细介绍与说明将在下面的部分给出。
    6. 对于项目中算法的进行流程。使用（A*+CBS）+SA算法体系的中心计算节点会向全局机器人发送任务说明，包括任务路径及执行时间。机器人通过信息的首发单元完成有关任务。
* 需要特别声明的是，本项目在环境设计和算法构思上还不完善，为了更好的效率和更优秀的可视化，本代码库也会持续更新。

