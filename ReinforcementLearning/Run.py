from matplotlib.colors import ListedColormap, BoundaryNorm

from Environment.Grid import Grid
from Trees.TreeGenerator import TreeGenerator
from GeneticAlgorithm.CustomGeneticChanges import CustomGeneticChanges
from GeneticAlgorithm.AlgorithmMutations import AlgorithmMutations
import numpy as np
import json

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

# Load the 2D array from the file
with open('Environment/apartment_grid.json', 'r') as f:
    apartment_grid = json.load(f)

shape = np.array(apartment_grid).shape
x = shape[1]
y = shape[0]


test = CustomGeneticChanges(x, y, tree_types_dict, TreeGenerator())
#test.test()

# Create the grid
env = Grid(x, y)
num_grid = np.zeros((y, x))
#make numeric grid. 1 is non plantable, 5 is plantable, 2 is hedge, 3 is large tree area, 4 by road
for i in range(y):
    for j in range(x):
        if apartment_grid[i][j] == 101 and env.grid[i][j].hedge:
            num_grid[i][j] = 2
        elif apartment_grid[i][j] == 63:
            num_grid[i][j] = 3
        elif apartment_grid[i][j] == 77:
            num_grid[i][j] = 4
        elif apartment_grid[i][j] == 101:
            num_grid[i][j] = 5
        elif apartment_grid[i][j] == 168:
            num_grid[i][j] = 6
        else:
            if env.grid[i][j].pedestrian_road:
                num_grid[i][j] = 6
            elif env.grid[i][j].plantable: num_grid[i][j] = 5
            elif env.grid[i][j].hedge: num_grid[i][j] = 2
            else: num_grid[i][j] = 1

#print the num_grid out
for row in num_grid:
    for square in row:
        print(square, end=' ')
    print()


import matplotlib.pyplot as plt

#visualize grid
cmap = ListedColormap(['green', 'white', 'yellow', 'red', 'blue', 'orange'])

# Define the boundaries
bounds = [0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5]

# Create the norm using BoundaryNorm
norm = BoundaryNorm(bounds, cmap.N)

# Create the plot
plt.figure(figsize=(19, 19))
plt.imshow(num_grid, cmap=cmap, norm=norm, aspect='equal')

# Add grid lines with correct alignment
plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
plt.xticks(np.arange(-0.5, len(num_grid[0]), 1), [])
plt.yticks(np.arange(-0.5, len(num_grid), 1), [])

# Setting grid lines for minor ticks to ensure they are in between cells
plt.gca().set_xticks(np.arange(-0.5, len(num_grid[0]), 1), minor=True)
plt.gca().set_yticks(np.arange(-0.5, len(num_grid), 1), minor=True)
plt.grid(True, which='minor', color='black', linestyle='-', linewidth=2)
plt.show()

generator = TreeGenerator()
x = 30
y = 30
COST_LIMIT = 40000
NUM_TREES = 21

custom_genetic = CustomGeneticChanges(x, y, tree_types_dict, generator)
#custom_genetic.run()

#env = Grid(x, y)
#mutate = AlgorithmMutations(tree_types_dict, env)

#mutate.plant_tree(1, 10, 10)
#env.print_grid()
#print("=========================")
#mutate.plant_tree(1, 11, 11)
#env.print_grid()


#fitness_eval = Constraints(x, y, COST_LIMIT, tree_types_dict, generator)
#mutations = AlgorithmMutations(tree_types_dict, env)
#greedy_alg = GreedyInitGrid(x, y, env, tree_types_dict, generator, fitness_eval, mutations)
#greedy_alg.init_grid(x, y)



#check if grid is valid
#grid = env.numerical_grid.flatten()
#fitness_eval.validate(grid)
#env.print_grid()
#mutations.visualize_grid()















'''
#loop through env. if square.plantable is false, print -1, if hedge, print 2, if large, print 3, else 0
for row in env.grid:
    for square in row:
        if not square.plantable:
            print(-1, end=' ')
        elif square.hedge:
            print(2, end=' ')
        elif square.big_tree_area:
            print(3, end=' ')
        else:
            print(0, end=' ')
    print()

#init start grid and validate that the grid abides constraints
start_grid = greedy_alg.init_grid(x, y)


#fitness_eval.validate(start_grid)
'''