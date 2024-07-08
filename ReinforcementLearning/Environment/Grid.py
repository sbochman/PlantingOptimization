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

    tree_types_dict1 = {
        0: "None",
        1: "Abies Holophylla",
        2: "Pinus Desniflora1",
        3: "Acer Palmatum",
        4: "Zelkova Serrata",
        5: "Cercidiphyllum Japonicum",
    }

    def __init__(self, x, y):
        """
        Constructor for the Grid class
        """
        self.x = x
        self.y = y
        self.landscape_area = x * y
        self.grid = self.create_grid(x, y)
        self.numerical_grid = np.zeros((x, y))
        self.state = np.zeros((x, y, 5)) # x, y, tree_type
        #self.initalize_state_grid()
        self.spots = self.x * self.y
        self.constraints = Constraints(self.spots) # Initialize constraints and plantable spots available
        #self.B = np.random.normal(scale=1/np.sqrt(2), size=(4, 2))
        #self.state = self.initialize_state_with_fourier_features()

        self.total_co2 = 0
        self.total_cost = 0

        self.co2_mean = 4.51
        self.co2_variance = 7.64
        self.co2_sd = np.sqrt(self.co2_variance)

        self.cost_mean = 745.38
        self.cost_variance = 581426.33
        self.cost_sd = np.sqrt(self.cost_variance)
        self.plantable_spots_remaining = self.spots

        self.cost_remaining = 10000
        self.tree_stats = [[0, 0], [(self.co2_mean - 2.2) / self.co2_sd, (self.cost_mean - 135) / self.cost_sd], [(self.co2_mean - 5.4) / self.co2_sd, (self.cost_mean - 1949) / self.cost_sd], [(self.co2_mean - 5.4) / self.co2_sd, (self.cost_mean - 281) / self.cost_sd],
                           [(self.co2_mean - 5.4) / self.co2_sd, (self.cost_mean - 1398) / self.cost_sd], [(self.co2_mean - 0.5) / self.co2_sd, (self.cost_mean - 1864) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 57) / self.cost_sd], [(self.co2_mean - 3.1) / self.co2_sd, (self.cost_mean - 796) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 279) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 423) / self.cost_sd],
                           [(self.co2_mean - 3.9) / self.co2_sd, (self.cost_mean - 381) / self.cost_sd], [(self.co2_mean - 3.5) / self.co2_sd, (self.cost_mean - 550) / self.cost_sd], [(self.co2_mean - 2.9) / self.co2_sd, (self.cost_mean - 211) / self.cost_sd], [(self.co2_mean - 4.5) / self.co2_sd, (self.cost_mean - 406) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 423) / self.cost_sd], [(self.co2_mean - 3.9) / self.co2_sd, (self.cost_mean - 389) / self.cost_sd],
                           [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 423) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 186) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 55) / self.cost_sd], [(self.co2_mean - 9.0) / self.co2_sd, (self.cost_mean - 576) / self.cost_sd], [(self.co2_mean - 3.8) / self.co2_sd, (self.cost_mean - 322) / self.cost_sd], [(self.co2_mean - 14.8) / self.co2_sd, (self.cost_mean - 1949) / self.cost_sd]]


    def initialize_state_with_fourier_features(self):
        """Initialize the grid state with Fourier features."""
        grid_x, grid_y = np.meshgrid(range(self.x), range(self.y), indexing='ij')
        flat_x = grid_x.flatten()
        flat_y = grid_y.flatten()
        fourier_features = self.generate_fourier_features(flat_x, flat_y, self.B)
        return fourier_features.reshape(self.x, self.y, -1)

    def generate_fourier_features(self, x, y, B):
        """
        Generate Fourier features for the coordinates x, y using frequency matrix B.

        Args:
            x (np.array): x coordinates of the grid.
            y (np.array): y coordinates of the grid.
            B (np.array): Frequency matrix of shape (num_features, 2).

        Returns:
            np.array: Array of Fourier features.
        """
        # Stack x and y for matrix multiplication
        xy = np.stack([x, y], axis=-1)  # Shape will be N x 2, where N is the number of points

        # Apply the Fourier transform
        projection = xy @ B.T  # Resulting shape will be N x num_features

        # Apply the sine and cosine transformations
        fourier_features = np.concatenate([np.sin(projection), np.cos(projection)], axis=-1)

        return fourier_features

    def create_grid(self, x, y):
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
                    self.landscape_area -= 1
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
        self.grid = self.create_grid(self.x, self.y)
        self.numerical_grid = np.zeros((self.x, self.y))
        self.initalize_state_grid()
        #self.initialize_state_with_fourier_features()
        self.constraints.total_co2 = 0
        self.constraints.above_co2_threshold = False
        self.constraints.number_co2_over_threshold = 0
        self.constraints.total_cost = 0
        self.constraints.below_cost_threshold = True
        self.constraints.plantable_spots_remaining = self.spots
        self.cost_remaining = 10000
        return self.state

    def get_possible_actions(self):
        """
        Get all possible actions (positions) in the grid where a tree can be planted.
        """
        return [(i, j) for i in range(self.x) for j in range(self.y) if self.grid[i, j].plantable]

    def get_plantable_positions_grid(self):
        return np.array([[1 if self.grid[i, j].plantable else 0 for j in range(self.y)] for i in range(self.x)])


    def step(self, action, x, y):
        # Check the structure of action and adjust accordingly
        generator = TreeGenerator()
        #loop through action and plant tree

        tree_type = int(action)
        self.plantable_spots_remaining -= 1


        tree = generator.generateTree(self.tree_types_dict[tree_type], (x, y))
        self.total_cost += tree.price
        self.total_co2 += tree.co2_absorption
        self.cost_remaining -= tree.getPrice()
        reward = self.constraints.calculate_reward(action, tree, self.grid, self.state)


        self.grid = self.plant(x, y, tree)


        self.update_state(x, y, tree_type, tree)


        #reward = 3 if tree_type in good_trees else -1
        if len(self.get_possible_actions()) == 0:
            done = True
        elif self.cost_remaining < 0:
            done = True
        else: done = False

        return self.state, reward, done


    def render(self):
        for i in range(self.x):
            for j in range(self.y):
                print(self.state[i][j][2], end=" ")
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

    def update_state(self, x, y, tree_type, tree):
        """
        Method to get the numerical representation of the grid
        :return: numerical grid
        """
        self.total_cost += tree.getPrice()
        self.total_co2 += tree.getCo2Absorption()
        self.state[x, y][0] = x
        self.state[x, y][1] = y
        self.state[x, y][2] = tree_type
        self.state[x, y][3] = (tree.getPrice() - self.cost_mean) / self.cost_sd
        if x < self.x -1 and y < self.y -1:
            self.state[x+1, y+1][4] = self.cost_remaining / 10000

    def get_state(self):
        return self.state

    def print_state(self):
        for i in range(self.x):
            for j in range(self.y):
                print(self.state[i, j][2], end=" ")
            print("")

    def initalize_state_grid(self):
        spots = self.x * self.y
        for i in range(self.x):
            for j in range(self.y):
                #self.state[i, j] = (i, j, 0, 0, 0, spots, 0, 0) # tree_type, plantable
                self.state[i, j] = (i, j, 0, spots / 30, 1) #x, y, tree_type, price, co2_absorption, all tree types co2 and price
                spots -= 1

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

