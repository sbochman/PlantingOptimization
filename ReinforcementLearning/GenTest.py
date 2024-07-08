from Trees.TreeGenerator import TreeGenerator
from Trees.Tree import Tree
import random
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

generator = TreeGenerator()

GRID_WIDTH = 6
GRID_HEIGHT = 5
COST_LIMIT = 35000
NUM_TREES = 21

creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximize the fitness
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()
toolbox.register("attr_tree", random.randint, 0, NUM_TREES)
toolbox.register("individual", tools.initRepeat, creator.Individual,
                 toolbox.attr_tree, n=GRID_WIDTH*GRID_HEIGHT)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evaluate(individual):
    total_cost = 0
    total_co2 = 0
    grid = [individual[i:i+ GRID_WIDTH] for i in range(0, len(individual), GRID_WIDTH)]

    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            tree = generator.generateTree(tree_types_dict[cell], (x, y))
            total_cost += tree.getPrice()
            total_co2 += tree.getCo2Absorption()

    if total_cost > COST_LIMIT:
        return -1,
    print("Total cost: ", total_cost)
    return total_co2,


toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutUniformInt, low=0, up=NUM_TREES, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Generate the initial population and run the genetic algorithm:
population = toolbox.population(n=250)
NGEN = 250
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
