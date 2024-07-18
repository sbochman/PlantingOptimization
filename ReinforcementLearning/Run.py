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

generator = TreeGenerator()
x = 335
y = 514
COST_LIMIT = 40000
NUM_TREES = 21

custom_genetic = CustomGeneticChanges(x, y, tree_types_dict, generator)
custom_genetic.run()







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