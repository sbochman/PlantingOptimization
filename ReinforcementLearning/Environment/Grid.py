import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors

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

    tree_types_dict1 = {
        0: "None",
        1: "Abies Holophylla",
        2: "Pinus Desniflora1",
        3: "Acer Palmatum",
        4: "Betula Platyphylla",
        5: "Cercidiphyllum Japonicum",
    }

    def __init__(self, x, y):
        """
        Constructor for the Grid class
        """
        self.x = x
        self.y = y
        self.landscapeArea = x * y
        self.grid = self.createGrid(x, y)
        self.numericalGrid = np.zeros((x, y))
        self.state = np.zeros((x, y, 2)) # x, y, tree_type
        self.initalize_state_grid()
        self.spots = self.x * self.y

    def createGrid(self, x, y):
        """
        Method to create a grid of squares
        :param x: x size of the grid
        :param y: y size of the grid
        :return: the grid
        """
        self.grid = np.empty((x, y), dtype=object)
        for i in range(x):
            for j in range(y):
                if i == 10 and j < 14:
                    self.grid[i, j] = Square(i, j, True, True)
                elif i > 6 and j > 8:
                    self.grid[i, j] = Square(i, j, False, False)
                    self.landscapeArea -= 1
                else:
                    self.grid[i, j] = Square(i, j, False, True)
        return self.grid

    def plant(self, x, y, tree):
        self.grid[x, y].plant(tree)
        return self.grid

    def reset(self):
        """
        Method to reset the grid
        :return: the grid
        """
        self.grid = self.createGrid(self.x, self.y)
        self.numericalGrid = np.zeros((self.x, self.y))
        self.initalize_state_grid()
        return self.state

    def get_possible_actions(self):
        """
        Get all possible actions (positions) in the grid where a tree can be planted.
        """
        return [(i, j) for i in range(self.x) for j in range(self.y) if self.grid[i, j].plantable]

    def get_plantable_positions_grid(self):
        return np.array([[1 if self.grid[i, j].plantable else 0 for j in range(self.y)] for i in range(self.x)])


    def step(self, action, x, y):
        previous_state = self.state.copy()
        good_trees = [2, 3, 7, 21]
        # Check the structure of action and adjust accordingly
        generator = TreeGenerator()
        #loop through action and plant tree
        reward = 0

        tree_type = int(action)


        if self.state[x, y][1] != 1 and action != 0 : reward -=5
        elif self.state[x, y][1] != 1 and action == 0: reward += 2
        elif tree_type in good_trees: reward += 5
        else: reward+=1

        tree = generator.generateTree(self.tree_types_dict[tree_type], (x, y))
        self.grid = self.plant(x, y, tree)
        self.updateState(x, y, tree_type)


        #reward = 3 if tree_type in good_trees else -1
        done = False  # Define a proper condition to update this

        return self.state, reward, done




    def render(self):
        for i in range(self.x):
            for j in range(self.y):
                print(self.state[i][j], end=" ")
            print()

        grid_copy = np.zeros((self.x, self.y))
        for i in range(self.x):
            for j in range(self.y):
                if self.grid[i, j].tree:
                    grid_copy[i, j] = 1  # Tree planted
                elif not self.grid[i, j].plantable and not self.grid[i, j].tree:
                    grid_copy[i, j] = -1  # Non-plantable area

        cmap = colors.ListedColormap(['white', 'red', 'green'])
        bounds = [-1.5, -0.5, 0.5, 1.5]
        norm = colors.BoundaryNorm(bounds, cmap.N)

        plt.imshow(grid_copy, cmap=cmap, norm=norm)
        plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
        plt.xticks(np.arange(-0.5, self.grid.shape[1], 1), [])
        plt.yticks(np.arange(-0.5, self.grid.shape[0], 1), [])
        plt.gca().set_xticks(np.arange(-0.5, self.grid.shape[1], 1), minor=True)
        plt.gca().set_yticks(np.arange(-0.5, self.grid.shape[0], 1), minor=True)
        plt.gca().grid(which='minor', color='black', linestyle='-', linewidth=2)
        plt.show()

    def updateState(self, x, y, tree_type):
        """
        Method to get the numerical representation of the grid
        :return: numerical grid
        """

        if self.state[x, y][1] != 1:
            return
        self.state[x, y] = (tree_type, 0)
        if x+1 < self.x:
            self.state[x+1, y] = (-1, -1)
        if x-1 >= 0:
            self.state[x-1, y] = (-1, -1)

    def get_state(self):
        return self.state

    def print_state(self):
        for i in range(self.x):
            for j in range(self.y):
                print(self.state[i, j], end=" ")
            print("")

    def initalize_state_grid(self):
        for i in range(self.x):
            for j in range(self.y):
                self.state[i, j] = (0, 1) # tree_type, plantable

    def calculate_reward(self, x, y, tree_type, is_spot_empty):
        # Define base rewards and penalties
        base_reward_empty = 10  # Reward for planting in an empty spot
        penalty_occupied = -30  # Penalty for planting in an occupied spot
        preferred_tree_bonus = 15  # Extra reward for preferred trees

        # Set of preferred tree types
        preferred_trees = {3, 5}

        # Check if the spot is empty
        if is_spot_empty:
            # Check if the tree type is preferred
            if tree_type in preferred_trees:
                reward = base_reward_empty + preferred_tree_bonus
            else:
                reward = base_reward_empty

        else:
            # Apply a penalty for planting in an occupied spot
            # Could scale with the number of plantings if that information is tracked
            reward = penalty_occupied

        return reward

