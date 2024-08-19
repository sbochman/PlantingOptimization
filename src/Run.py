from matplotlib.colors import ListedColormap, BoundaryNorm
from Environment.Grid import Grid
from Trees.TreeGenerator import TreeGenerator
from GeneticAlgorithm.CustomGeneticChanges import CustomGeneticChanges
import numpy as np


def main():
    """
    This function is used to run the genetic algorithm and display the results. It will also display the grid with the trees
    """
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

    tree_types_edi_dict = {
        0: "None",
        1: "Abies Holophylla",
        5: "Taxus Cuspidata",
        6: "White Pine",
        7: "Acer Palmatum",
        8: "Betula Platyphylla",
        9: "Cercidiphyllum Japonicum",
        11: "Chionanthus Retusus",
        12: "Cornus Officinalis",
        13: "Ginkgo Biloba",
        14: "Kobus Magnolia",
        15: "Liriodendron Tulipifera",
        16: "Oak",
        17: "Persimmon",
        18: "Prunus Armeniaca",
        20: "Sophora Japonica",
        21: "Zelkova Serrata"
    }

    #create tree generator
    generator = TreeGenerator()
    x = 335
    y = 514
    COST_LIMIT = 60000
    NUM_TREES = 16

    #run the genetic algorithm
    custom_genetic = CustomGeneticChanges(x, y, tree_types_dict, generator, 1)
    custom_genetic.run_scenario_one()
    #custom_genetic = CustomGeneticChanges(x, y, tree_types_dict, generator, 2)
    #custom_genetic.run_scenario_two()


    import matplotlib.pyplot as plt
    env = Grid(x, y, 2)

    #make numerical grid of env
    numerical_grid = np.zeros((y, x))
    for i in range(y):
        for j in range(x):
            if j > 316:
                numerical_grid[i][j] = 2
            if env.grid[i][j].hedge:
                numerical_grid[i][j] = 2
            elif env.grid[i][j].big_tree_area:
                numerical_grid[i][j] = 3
            elif env.grid[i][j].road:
                numerical_grid[i][j] = 4
            elif env.grid[i][j].pedestrian_road:
                numerical_grid[i][j] = 5
            elif env.grid[i][j].plantable:
                numerical_grid[i][j] = 1
            else:
                numerical_grid[i][j] = 0



    #print the grid. a different color for each plantable region.
    #0 is unplantable, 1 is plantable, 2 is hedge, 3 is large tree area, 4 is road, 5 is pedestrian road
    #cmap = ListedColormap(['white', 'blue', 'purple', 'red', 'green', 'orange'])
    #bounds = [-0.5, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    #norm = BoundaryNorm(bounds, cmap.N)
    #plt.figure(figsize=(9, 9))
    #plt.imshow(numerical_grid, cmap=cmap, norm=norm, aspect='equal')
    #plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
    #plt.show()

if __name__ == "__main__":
    main()