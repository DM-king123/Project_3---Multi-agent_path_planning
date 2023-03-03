import operator

# 资源需求点和对应的需求量
demand = {
    1: 80,
    2: 50,
    3: 230,
    4: 50,
    5: 130,
    6: 830,
    7: 130,
    8: 280,
    10: 180,
    12: 50,
    17: 500,
    18: 100,
    19: 100,
    20: 80,
    21: 200,
    22: 80,
    23: 290,
    24: 76,
    26: 36,
    28: 56,
    29: 380,
    31: 80,
    34: 148,
    36: 62,
    37: 66,
    41: 220,
    42: 220,
    43: 80,
    44: 150,
    45: 530,
    46: 120,
    51: 120,
    53: 250
}

# 每家医院的资源总数
hospital_capacity = 10000

# 每辆运输车的载荷
truck_capacity = 150

# 初始化每个运输车的任务列表
num_trucks = int(sum(demand.values()) / truck_capacity) + 1
truck_tasks = [[] for _ in range(num_trucks)]

# 按照需求量从大到小排序
sorted_demand = sorted(demand.items(), key=operator.itemgetter(1), reverse=True)

# 分配任务
for d in sorted_demand:
    demand_amount = d[1]
    assigned = False
    # 对每个运输车进行容量限制检查
    for i in range(num_trucks):
        if sum(truck_tasks[i]) + demand_amount <= truck_capacity:
            truck_tasks[i].append(d[0])
            assigned = True
            break
    # 如果找不到可用运输车，则分配失败
    if not assigned:
        print(f"Resource demand point {d[0]} cannot be assigned to any truck.")

# 对每个医院进行需求点分配
hospitals = {}
for d in sorted_demand:
    demand_amount = d[1]
    hospital_id = d[0] // 10  # 假设每家医院的需求点编号都以10的倍数递增
    if hospital_id not in hospitals:
        hospitals[hospital_id] = []
    if sum(hospitals[hospital_id]) + demand_amount <= hospital_capacity:
        hospitals[hospital_id].append(d[0])
    else:
        print(f"Resource demand point {d[0]} cannot be assigned to hospital {hospital_id}.")

# 输出结果
for i, t in enumerate(truck_tasks):
    print(f"Truck {i+1}: {t}")
for h, d in hospitals.items():
    print(f"Hospital {h}: {[x % 10 for x in d]}")
