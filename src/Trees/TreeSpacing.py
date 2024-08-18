import numpy as np
from Trees.TreeGenerator import TreeGenerator
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class TreeSpacing:
    """
    This class is used to confirm the tree spacing requirements for each tree type. Each tree has a different radius.
    This class ensures that the radius is respected when trying to plant another tree. It can also remove trees. All changes
    are logged in the Grid object.

    Attributes:
        tree_types_dict (dict): a dictionary with keys as the tree number and values as the tree
    """

    def __init__(self, tree_types_dict):
        """
        Constructor for TreeSpacing class

        :param tree_types_dict (dict): a dictionary with keys as the tree number and values as the tree
        """
        self.tree_types_dict = tree_types_dict

    def update_coords(self, fill_cords, grid, numerical_representation, center, env):
        """
        This function updates the grid with the new tree. It checks if the tree can be planted in the given location.

        :param fill_cords (list): a list of coordinates that are occupied by the tree
        :param grid (numpy array): the grid that is being updated. the numerical representation
        :param numerical_representation (numpy array): the numerical representation of the tree
        :param center (int, int): the center of the tree (x, y) coordinates
        :param env (Grid object): the grid object that is being updated
        :return: numpy array grid, boolean plantable
        """
        plantable = True
        for coord in fill_cords:
            y, x = coord
            if grid[y][x] != 0 or env.grid[y][x].is_plantable() is False:
                plantable = False
                break
        if plantable:
            for coord in fill_cords:
                y, x = coord
                grid[y][x] = numerical_representation #change grid of surrounding tree radius to negative (occupied)
            x, y = center
            grid[y][x] = abs(numerical_representation) #change base of tree to its positive representation
        return grid, plantable

    def remove_tree(self, fill_cords, grid, env):
        """
        This function removes a tree from the grid. It updates the grid and the environment object.

        :param fill_cords (list): a list of coordinates that are occupied by the tree
        :param grid (numpy array): the grid that is being updated. the numerical representation
        :param env (Grid object): the grid object that is being updated
        :return: grid (numpy array)
        """
        for coord in fill_cords:
            y, x = coord
            grid[y][x] = 0
            env.grid[y][x].tree = None
            env.grid[y][x].plantable = True
        return grid

    def generate_tree_radius_png(self):
        """
        This function generates a png for each tree type. The png shows the tree radius for each tree.
        """

        #loop through all trees, create a grid for each tree, and save the grid as a png
        for i in range(1, 22):
            #crate tree
            grid = np.zeros((9, 9))
            tree = TreeGenerator().generateTree(self.tree_types_dict[i], (4, 4))
            occupied, numerical_representation = tree.returnOccupiedSpots()
            grid, plantable = self.update_coords(occupied, grid, numerical_representation, tree.getPlantingLocation())

            # Define a color map: 1 is green and 0 is white
            cmap = ListedColormap(['green', 'white'])

            plt.figure(figsize=(9, 9))
            plt.imshow(grid, cmap=cmap, aspect='equal')  # Use the color map

            # Add grid lines with correct alignment
            plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
            plt.xticks(np.arange(-0.5, len(grid[0]), 1), [])
            plt.yticks(np.arange(-0.5, len(grid), 1), [])

            # Setting grid lines for minor ticks to ensure they are in between cells
            plt.gca().set_xticks(np.arange(-0.5, len(grid[0]), 1), minor=True)
            plt.gca().set_yticks(np.arange(-0.5, len(grid), 1), minor=True)
            plt.grid(True, which='minor', color='black', linestyle='-', linewidth=2)

            plt.title(self.tree_types_dict[i] + ' Grid Spatial Visualization: Green Planted, White Unplanted')
            #save the grid as a png
            filename = self.tree_types_dict[i].replace(' ', '_') + '.png'
            plt.savefig('ReinforcementLearning/Trees/TreeSpatialGridVisualization/' + filename)


