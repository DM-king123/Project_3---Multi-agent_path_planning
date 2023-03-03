import random
import numpy as np

# 此代码定义了问题参数、遗传算法参数以及基因和染色体表示。
# NUM_HOSPITALSVEHICLE_CAPACITY和NUM_DEMAND_POINTS变量定义问题参数。
# 这里的POPULATION_SIZE, NUM_GENERATIONS,ELITE_SIZE，'TOURNAMENT_SIZETOURNAMENT_SIZE,MUTATION_RATE和“CROSSOVER_RATECROSSOVER_RATE变量定义遗传算法参数。
# 基因和染色体表示将在代码的后面定义
# Define the problem parameters
NUM_HOSPITALS = 3
HOSPITALS_CAPACITY = 10000
NUM_VEHICLES = 40
VEHICLE_CAPACITY = 150
NUM_DEMAND_POINTS = 33
DEMAND_QUANTITY = {
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
# create demand dictionary
demand_dict = {}
for demand_point, demand in DEMAND_QUANTITY.items():
    demand_dict[demand_point] = demand

# create hospital dictionary
hospital_dict = {}
for i in range(NUM_HOSPITALS):
    hospital_dict[i] = {
        "capacity": HOSPITALS_CAPACITY,
    }

# create transport dictionary
transport_dict = {}
for i in range(NUM_VEHICLES):
    transport_dict[i] = {
        "capacity": VEHICLE_CAPACITY[i]
    }


# Define the parameters for the genetic algorithm
POPULATION_SIZE = 100
NUM_GENERATIONS = 100
ELITE_SIZE = 20
TOURNAMENT_SIZE = 5
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.5
# Define the gene and chromosome representation
# Each gene represents the hospital to which a demand point is assigned
# Each chromosome represents a solution to the problem


# 基因和染色体的创建函数。
# 染色体中的每个基因代表分配需求点的医院。
# 这里的create_individual()函数通过将医院随机分配到请求点来创建单个单独的染色体。
# 这里的create_population()函数通过多次调用create_individual()创建个体群体。
# Define the gene and chromosome representation
# Each gene represents the hospital to which a demand point is assigned
# Each chromosome represents a solution to the problem
def create_individual():
    individual = []
    for i in range(NUM_DEMAND_POINTS):
        individual.append(random.randint(0, NUM_HOSPITALS - 1))
    return individual

def create_population():
    population = []
    for i in range(POPULATION_SIZE):
        population.append(create_individual())
    return population

#此代码定义evaluate_fitness()函数，计算单个染色体的适应性。
# fitness函数将单个染色体作为输入并返回fitness值。
# fitness函数通过对分配给该医院的所有需求点的需求求和来计算该医院的需求。
# 然后，它通过对每家医院的需求超过所有车辆的总容量进行求和来计算适用度。
# 如果任何医院的需求超过所有车辆的总容量，则fitness值将增加超额需求量。
# Define the fitness function
def evaluate_fitness(individual):
    hospital_demands = [0] * NUM_HOSPITALS
    vehicle_demands = [0] * NUM_VEHICLES
    fitness = 0
    
    for i in range(NUM_DEMAND_POINTS):
        hospital = individual[i]
        demand = DEMAND_QUANTITY[i + 1]
        hospital_demands[hospital] += demand
        
    for i in range(NUM_HOSPITALS):
        if hospital_demands[i] > VEHICLE_CAPACITY * NUM_VEHICLES:
            fitness += hospital_demands[i] - VEHICLE_CAPACITY * NUM_VEHICLES
            
    return fitness

#定义选择函数
# Define the selection function
def select_parents(population):
    parents = []
    total_fitness = 0
    
    for individual in population:
        fitness = evaluate_fitness(individual)
        total_fitness += fitness
    
    for i in range(2):
        r = random.uniform(0, total_fitness)
        temp_sum = 0
        for individual in population:
            fitness = evaluate_fitness(individual)
            temp_sum += fitness
            if temp_sum >= r:
                parents.append(individual)
                break
                
    return parents

# 此代码定义crossover()函数，对两条亲本染色体执行交叉以创建两条后代染色体。
# 该函数将两条父染色体的列表作为输入，并返回两条后代染色体的列表。
# 交叉函数首先在第一个和最后一个请求点之间选择一个随机交叉点。
# 然后，它通过将第一条亲本染色体的第一部分与第二条亲本染色体的第二部分结合起来来创建两条后代染色体，反之亦然。
# 该函数返回列表中的两条后代染色体。
# Define the crossover function
def crossover(parents):
    offspring = []
    parent1 = parents[0]
    parent2 = parents[1]
    crossover_point = random.randint(1, NUM_DEMAND_POINTS - 1)
    offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
    offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
    offspring.append(offspring1)
    offspring.append(offspring2)
    return offspring

# 此代码定义mutation()函数，使群体中的单个染色体发生突变。
# 该函数将单个染色体作为输入并返回突变的染色体。
# 突变函数迭代染色体中的每个需求点，并且概率MUTATION_RATE，将分配给该请求点的医院替换为随机选择的医院。
# 如果未为突变选择请求点，则函数只需将值从原始染色体复制到突变的染色体。
# 该函数返回突变的染色体。
# Define the mutation function
def mutation(individual):
    mutated_individual = []
    for i in range(NUM_DEMAND_POINTS):
        if random.uniform(0, 1) < MUTATION_RATE:
            mutated_individual.append(random.randint(1, NUM_HOSPITALS))
        else:
            mutated_individual.append(individual[i])
    return mutated_individual

#此代码定义evolve()函数，执行遗传算法的一次迭代。
# 该函数将当前总体作为输入并返回新的总体。
# 进化函数首先创建一个空列表来存储新种群。
# 然后，它对总体中的每对父项执行以下步骤：
        #使用“select_parents选择两条亲本染色体
        #通过使用执行交叉来创建两条后代染色体
        #将两条突变的后代染色体添加到新群体中。
        #该函数在处理完当前种群中的所有父项对后返回新种群。
# Define the evolution function
def evolve(population):
    new_population = []
    for i in range(POPULATION_SIZE // 2):
        parents = select_parents(population)
        offspring = crossover(parents)
        mutated_offspring1 = mutation(offspring[0])
        mutated_offspring2 = mutation(offspring[1])
        new_population.append(mutated_offspring1)
        new_population.append(mutated_offspring2)
    return new_population

# 运行指定世代数的遗传算法。
# 完成指定的代数后，算法终止，优化期间发现的最佳单个染色体是问题的解决方案。
# 在这种情况下，最佳单个染色体代表一组满足每个资源需求点需求的医院分配。
# Run the genetic algorithm
def initialize_population(population_size, num_demand_points, num_hospitals):
    population = []
    for i in range(population_size):
        individual = np.random.randint(0, num_hospitals, num_demand_points)
        population.append(individual)
    return population

population = initialize_population(POPULATION_SIZE, NUM_DEMAND_POINTS, NUM_HOSPITALS)
for i in range(NUM_GENERATIONS):
    fitness_values = evaluate_fitness(population, demand_dict, hospital_dict, transport_dict)
    best_individual = population[np.argmin(fitness_values)]
    print(f"Generation {i+1}: Best fitness = {1/np.min(fitness_values):.2f}")
    population = evolve(population)

# 此代码打印遗传算法找到的解决方案。
# 以“资源请求点 [编号] 分配给医院 [编号]”的格式打印每个资源请求点的医院分配。
# Print the solution
print("\nSolution:")
for i in range(NUM_DEMAND_POINTS):
    print(f"Resource demand point {i+1} is assigned to hospital {best_individual[i]}")
