import numpy as np
from Landscape.Square import Square

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
        grid = np.empty((y, x), dtype=object)  # Swap x and y here
        for i in range(y):
            for j in range(x):
                if i == 9:
                    grid[i, j] = Square(j, i, False, True, True, False, False)
               # elif i == 2 and j == 2:
               #     grid[i, j] = Square(j, i, False, False, False, False, False)
                else:
                    grid[i, j] = Square(j, i, False, True, False, False, False)
        return grid

    def create_numerical_grid(self, x, y):
        """
        Method to create a grid of numerical values
        :param x: x size of the grid
        :param y: y size of the grid
        :return: the numerical grid
        """
        numerical_grid = np.empty((y, x), dtype=int)
        for i in range(y):
            for j in range(x):
                numerical_grid[i, j] = 0
        return numerical_grid

    def plant(self, x, y, tree):
        """
        Method to plant a tree on a square
        :param x: x coordinate
        :param y: y coordinate
        :param tree: tree object to plant
        :return: the grid with updated tree planted
        """
        self.grid[y, x].plant(tree)
        return self.grid

    def print_grid(self):
        """
        Method to print the grid
        """
        for i in range(self.y):
            for j in range(self.x):
                print(self.numerical_grid[i, j], end=" ")
            print()

