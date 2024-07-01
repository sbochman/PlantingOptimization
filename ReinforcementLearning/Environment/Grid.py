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

    def __init__(self, x, y):
        """
        Constructor for the Grid class
        """
        self.x = x
        self.y = y
        self.landscapeArea = x * y
        self.grid = self.createGrid(x, y)
        self.numericalGrid = np.zeros((x, y))
        self.rewardGrid = np.zeros((x, y))
        self.neuralGrid = np.zeros((x, y, 3))  # 0: Plantable, 1: Tree Type, 2: Reward
        # Initialize (could add more sophisticated initialization as needed)
        self.neuralGrid[:, :, 0] = -1  # Default no tree planted
        self.neuralGrid[:, :, 1] = 0   # Default reward
        self.neuralGrid[:, :, 2] = 0   # Default plantable

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

    def plot_grid(self, qTable):
        """
        Plots the grid using Matplotlib.
        - Good planting spots (where trees are planted) are green.
        - Bad planting spots (whether planted or not) are red.
        - Bad planting spots (where trees are planted) are orange.
        - Unplanted spots remain white.
        """
        # Create a copy of the grid for plotting
        grid_copy = self.grid.copy()

        for i in range(len(grid_copy)):
            for j in range(len(grid_copy[i])):
                action = self.get_best_action_for_spot((i, j), qTable)
                print(action, end=" ")
                if action == 1 and (i, j) in self.bad_plant_positions:  # Tree planted in a bad spot
                    grid_copy[i][j] = 3  # Mark it as orange (3)
                elif action == 1:  # Good spot with a tree
                    grid_copy[i][j] = 1  # Mark it as green (1)
                elif action == -1 and (i, j) in self.bad_plant_positions:  # Bad spot but not planted
                    grid_copy[i][j] = 2  # Mark it as red (2)
                else:  # Unplanted spot
                    grid_copy[i][j] = 0  # Mark it as white (0)
            print()

        print("--------------------")

        # make the grid_copy a numpy array
        grid_copy = np.array(grid_copy)
        # print out the values in grid_copy
        for i in range(len(grid_copy)):
            for j in range(len(grid_copy[i])):
                print(grid_copy[i][j], end=" ")
            print()
        # Define a colormap with four colors: white, green, red, orange
        cmap = colors.ListedColormap(['green', 'red', 'orange'])

        plt.figure(figsize=(8, 8))
        plt.imshow(grid_copy, cmap=cmap, interpolation="none")
        plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
        plt.xticks(np.arange(-0.5, self.grid.shape[1], 1), [])
        plt.yticks(np.arange(-0.5, self.grid.shape[0], 1), [])
        plt.gca().set_xticks(np.arange(-0.5, self.grid.shape[1], 1), minor=True)
        plt.gca().set_yticks(np.arange(-0.5, self.grid.shape[0], 1), minor=True)
        plt.gca().grid(which='minor', color='black', linestyle='-', linewidth=2)
        # plt.gca().invert_yaxis()
        plt.savefig('grid.png')  # Save the plot as an image
        plt.show(block=True)  # Keep the plot open to inspect

    def reset(self):
        """
        Method to reset the grid
        :return: the grid
        """
        self.grid = self.createGrid(self.x, self.y)
        self.numericalGrid = np.zeros((self.x, self.y))
        return self.grid

    def get_possible_actions(self):
        """
        Get all possible actions (positions) in the grid where a tree can be planted.
        """
        return [(i, j) for i in range(self.x) for j in range(self.y) if self.grid[i, j].plantable]

    def get_plantable_positions_grid(self):
        return np.array([[1 if self.grid[i, j].plantable else 0 for j in range(self.y)] for i in range(self.x)])

    def get_observation(self):
        plantable_grid = self.get_plantable_positions_grid()
        return np.concatenate((self.numericalGrid.flatten(), plantable_grid.flatten())).astype(np.float32)

    def step(self, action):
        """
        Perform an action in the environment.

        Parameters:
        - action: a tuple (coordinates, tree_type) where coordinates is a tuple (x, y) and tree_type is an integer.

        Returns:
        - state: the new state after performing the action.
        - reward: the reward received after performing the action.
        - done: a boolean indicating if the episode is done.
        """

        # Unpack the action
        x, y, tree_type = action

        # Set of preferred tree types
        preferred_trees = {2, 3, 7, 21}

        if self.grid[x, y].plantable and self.grid[x, y].tree is None:
            tree_generator = TreeGenerator()
            species = Grid.tree_types_dict[tree_type]
            tree = tree_generator.generateTree(species, (x, y))
            self.plant(x, y, tree)
            self.updateNumericalGrid(x, y)
            self.rewardGrid[x][y] = tree.creditValue
            self.updateNeuralGrid(x, y, tree, tree_type)

            # Adjust reward based on tree type
            if tree.species != "None":
                if tree_type in preferred_trees:
                    reward = 4 * tree.creditValue  # Higher multiplier for preferred trees
                else:
                    reward = tree.creditValue - 4  # Small penalty for non-preferred trees
            else:
                reward = -5
        else:
            reward = -10  # Larger penalty for invalid actions

        done = len(self.get_possible_actions()) == 0  # Episode ends if all cells are filled
        return self.numericalGrid, reward, done


    def plantableSpaces(self):
        """
        Method to get the number of plantable spaces in the grid
        :return: count of plantable spaces
        """
        plantableSpaces = 0
        for i in range(self.x):
            for j in range(self.y):
                if self.grid[i, j].plantable:
                    plantableSpaces += 1
        return plantableSpaces

    def render(self):

        for i in range(self.x):
            for j in range(self.y):
                print(self.numericalGrid[i][j], end=" ")
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

    def updateNumericalGrid(self, x, y):
        """
        Method to get the numerical representation of the grid
        :return: numerical grid
        """
        self.numericalGrid[x, y] = self.grid[x, y].getNumericRepresentation()

    def get_state(self):
        # plantable_grid = self.get_plantable_positions_grid().flatten()
        #tree_grid = self.numericalGrid.flatten()
        #get credit value from the tree obj in each cell
        #reward_grid = np.zeros((self.x, self.y))
        # for i in range(self.x):
        # #     for j in range(self.y):
        #         if self.grid[i, j].tree:
        #             reward_grid[i, j] = self.grid[i, j].tree.creditValue

        # reward_grid = reward_grid.flatten()
        # return np.concatenate((plantable_grid, tree_grid, reward_grid)).astype(np.float32)
        return self.numericalGrid

    def decode_action(self, action):
        tree_types_count = len(Grid.tree_types_dict)
        cell_index = action // tree_types_count
        tree_type = action % tree_types_count
        x = cell_index // self.y
        y = cell_index % self.y
        return x, y, tree_type

    def print_reward_grid(self):
        for i in range(self.x):
            for j in range(self.y):
                print(self.rewardGrid[i][j], end=" ")
            print()

    def updateNeuralGrid(self, x, y, tree, tree_type):
        """
        Method to update the neural grid with the tree's properties
        :return: the updated neural grid
        """
        self.neuralGrid[x, y, 0] = tree_type
        self.neuralGrid[x, y, 1] = tree.creditValue
        self.neuralGrid[x, y, 2] = 1

