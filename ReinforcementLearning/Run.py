from GeneticAlgorithm.GreedyInitGrid import GreedyInitGrid
from ScenarioTwoConstraints.Constraints import Constraints
from Trees.TreeGenerator import TreeGenerator

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
x = 10
y = 10
COST_LIMIT = 40000
NUM_TREES = 21

greedy_alg = GreedyInitGrid(x, y)

fitness_eval = Constraints(x, y, COST_LIMIT, tree_types_dict, generator)

#init start grid and validate that the grid abides constraints
start_grid = greedy_alg.init_grid(x, y)
fitness_eval.validate(start_grid)