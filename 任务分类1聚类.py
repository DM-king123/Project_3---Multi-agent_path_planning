from sklearn.cluster import KMeans
import numpy as np

# 构造资源需求数据
demand_data = {
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

# 构造数据点数组
X = np.array([[demand_data[i]] for i in demand_data])

# 执行 KMeans 聚类
kmeans = KMeans(n_clusters=40)
kmeans.fit(X)

# 打印各个簇中心点的位置
print(kmeans.cluster_centers_)

# 打印每个资源需求点所属的簇
print(kmeans.labels_)

# 根据聚类结果生成运输车路径
paths = [[] for _ in range(40)]
for i, label in enumerate(kmeans.labels_):
    paths[label].append(i+1)

# 打印运输车路径
print(paths)
