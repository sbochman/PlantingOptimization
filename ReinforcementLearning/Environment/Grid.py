import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

from ScenarioTwoConstraints.Constraints import Constraints
from Landscape.Square import Square
#from ScenarioConstraints.ScenarioOneConstraints import ScenarioOneConstraints
from Trees.TreeGenerator import TreeGenerator
from Trees.Tree import Tree

class Grid:
    # define a dictionary of tree types of number -> tree type
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



    def __init__(self, x, y):
        """
        Constructor for the Grid class
        """
        self.x = x
        self.y = y
        self.landscape_area = x * y
        self.grid = self.create_grid(x, y)
        self.numerical_grid = self.create_numerical_grid(x, y)

    def create_grid(self, x, y):
        """
        Method to create a grid of squares
        :param x: x size of the grid
        :param y: y size of the grid
        :return: the grid
        """
        self.grid = np.empty((x, y), dtype=object)
        for i in range(y):
            for j in range(x):
                if i == 9:
                    self.grid[i, j] = Square(i, j, False, True, True, False, False)
                else:
                    self.grid[i, j] = Square(i, j, False, True, False, False, False)
        return self.grid

    def create_numerical_grid(self, x, y):
        """
        Method to create a grid of numerical values
        :param x: x size of the grid
        :param y: y size of the grid
        :return: the numerical grid
        """
        self.grid = np.empty((x, y), dtype=int)
        for i in range(x):
            for j in range(y):
                self.grid[i, j] = 0
        return self.grid

    def plant(self, x, y, tree):
        """
        Method to plant a tree on a square
        :param x: x coordinate
        :param y: y coordinate
        :param tree: tree object to plant
        :return: the grid with updated tree planted
        """
        self.grid[x, y].plant(tree)
        return self.grid

