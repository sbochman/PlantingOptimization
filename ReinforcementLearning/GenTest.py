from Trees.TreeGenerator import TreeGenerator
from Trees.Tree import Tree
from Environment.Grid import Grid
import random
import numpy as np
from ScenarioTwoConstraints.Constraints import Constraints
from deap import base, creator, tools, algorithms
random.seed(100)

tree_types_dict = {
    0: "None",
    1: "Abies Holophylla",
    2: "Pinus Desniflora1",
    3: "Pinus Desniflora2",
    4: "Pinus Desniflora Globosa",
    5: "Taxus Cuspidata",
    6: "White Pine",
    7: "Acer Palmatum",
    8: "Betula Platyphylla",
    9: "Cercidiphyllum Japonicum",
    10: "Chaenomeless Sinensis",
    11: "Chionanthus Retusus",
    12: "Cornus Officinalis",
    13: "Ginkgo Biloba",
    14: "Kobus Magnolia",
    15: "Liriodendron Tulipifera",
    16: "Oak",
    17: "Persimmon",
    18: "Prunus Armeniaca",
    19: "Prunus Yedoensis",
    20: "Sophora Japonica",
    21: "Zelkova Serrata"
}


def custom_cxTwoPoint(ind1, ind2):
    size = min(len(ind1), len(ind2))
    cxpoint1, cxpoint2 = sorted(random.sample(range(1, size), 2))
    for i in range(cxpoint1, cxpoint2):
        val = random.choice([1, 3])
        if val == 1 and ind1[i] != 0 and ind2[i] != 0:  # Skip if original value is 0
            ind1[i], ind2[i] = ind2[i], ind1[i]
        else:
            ind1[i], ind2[i] = ind2[i], ind1[i]

    # Ensure first row and column are not changed
    for i in range(GRID_WIDTH):
        ind1[i] = ind2[i] = 0
    for i in range(GRID_HEIGHT):
        ind1[i * GRID_WIDTH] = ind2[i * GRID_WIDTH] = 0

    return ind1, ind2

def custom_mutUniformInt(individual, low, up, indpb):
    size = len(individual)
    for i in range(size):
        if individual[i] != 0:  # Skip if original value is 0
            if random.random() < indpb:
                if not (i % GRID_WIDTH == 0 or i < GRID_WIDTH):  # Avoid first row and column
                    individual[i] = random.randint(low, up)
    return individual,


env = Grid(10, 10) #use the grid to create numeric

def init_grid(x, y):
    grid = []
    for i in range(x):
        for j in range(y):
            pass
    return grid

def get_tree_generator(start_grid):
    def predefined_tree():
        return [tree for tree in start_grid]
    return predefined_tree

generator = TreeGenerator()
GRID_WIDTH = 8
GRID_HEIGHT = 10
COST_LIMIT = 40000
NUM_TREES = 21

fitness_eval = Constraints(GRID_WIDTH, GRID_HEIGHT, COST_LIMIT, tree_types_dict, generator)

#init start grid and validate that the grid abides constraints
start_grid = init_grid(GRID_WIDTH, GRID_HEIGHT)
fitness_eval.validate(start_grid)

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximize the fitness
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
#toolbox.register("attr_tree", lambda: next(generation_one))
toolbox.register("individual", tools.initIterate, creator.Individual,
                 get_tree_generator(start_grid))   #, n=GRID_WIDTH*GRID_HEIGHT)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", fitness_eval.evaluate)
toolbox.register("mate", custom_cxTwoPoint)
toolbox.register("mutate", custom_mutUniformInt, low=0, up=NUM_TREES, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Generate the initial population and run the genetic algorithm:
population = toolbox.population(n=250)
NGEN = 500
for gen in range(NGEN):
    offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
    fits = toolbox.map(toolbox.evaluate, offspring)
    for fit, ind in zip(fits, offspring):
        ind.fitness.values = fit
    population = toolbox.select(offspring, k=len(population))

# Find and print the best solution found:
best_ind = tools.selBest(population, 1)[0]
print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))


def individual_to_grid(individual, width, height):
    return [individual[i:i + width] for i in range(0, len(individual), width)]

# Convert the best individual into a grid
best_grid = individual_to_grid(best_ind, GRID_WIDTH, GRID_HEIGHT)

# Print the grid
for row in best_grid:
    print(row)

fitness_eval.validate(best_ind)

# Optionally, you can also visualize the grid using matplotlib if you want to see it as an image
import matplotlib.pyplot as plt
import numpy as np

def plot_grid(grid):
    array = np.array(grid)
    plt.figure(figsize=(10, 8))
    plt.imshow(array, cmap='viridis', interpolation='nearest')
    plt.colorbar(label='Tree Types')
    plt.title('Planting Grid Visualization')
    plt.show()

plot_grid(best_grid)
