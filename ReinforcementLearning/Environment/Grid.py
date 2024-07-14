import numpy as np
import json
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
        with open("Environment/apartment_grid.json", "r") as f:
            self.apartment_grid = np.array(json.load(f))
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
                if self.apartment_grid[i, j] == 101 and (j > 314 or i < 22): #yellow grayscale value
                    grid[i, j] = Square(j, i, False, True, True, False, False)
                elif self.apartment_grid[i, j] == 63: #red grayscale value
                    grid[i, j] = Square(j, i, False, True, False, True, False)
                elif self.apartment_grid[i, j] == 77: #green grayscale value
                    grid[i, j] = Square(j, i, True, True, False, False, False)
                elif self.apartment_grid[i, j] == 101: #blue grayscale value
                    grid[i, j] = Square(j, i, False, True, False, False, False)
                elif self.apartment_grid[i, j] == 168: #orange grayscale value
                    grid[i, j] = Square(j, i, False, True, False, False, True)
                else: #non plantable area
                    grid[i, j] = Square(j, i, False, False, False, False, False)

        #hard coding problem cells
        #(161, 63)     (166, 63)
        #(161, 107)     (166, 107)
        #loop between these coordinates and set square to be by pedestrian_road
        for i in range(63, 108): #fixing pedestiran road that is not set
            for j in range(161, 167):
                grid[i, j].pedestrian_road = True

        #(167, 101)     (274, 101)
        #(167, 106)     (274, 106)
        #loop between these coordinates and set square to be by plantable
        for i in range(101, 107):
            for j in range(167, 275):
                grid[i, j].plantable = True

        #(75, 142)      (77, 142)
        #(75, 189)      (77, 189)
        for i in range(142, 190):
            for j in range(75, 78):
                grid[i, j].plantable = True

        #(40, 254)     (141, 254)
        #(40, 259)     (141, 259)
        for i in range(254, 260):
            for j in range(40, 142):
                grid[i, j].plantable = True

        #(167, 393)    (170, 393)
        #(167, 427)    (170, 427)
        for i in range(393, 428):
            for j in range(167, 171):
                grid[i, j].plantable = True

        #(170, 427)    (314, 427)
        #(170, 432)    (314, 432)
        for i in range(427, 433):
            for j in range(170, 315):
                grid[i, j].plantable = True

        #(162, 279)   (167, 279)
        #(162, 324)   (167, 324)
        for i in range(279, 325):
            for j in range(162, 168):
                grid[i, j].pedestrian_road = True

        #(167, 319)   (314, 319)
        #(167, 323)   (314, 323)
        for i in range(319, 324):
            for j in range(167, 315):
                grid[i, j].plantable = True


        #(318, 21)   (324, 21)
        #(318, 438)   (324, 438)
        for i in range(21, 439):
            for j in range(318, 325):
                grid[i, j].hedge = True


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

