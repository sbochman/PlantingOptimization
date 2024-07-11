import numpy as np
from Trees.TreeGenerator import TreeGenerator
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

class TreeSpacing:

    def __init__(self, tree_types_dict):
        self.tree_types_dict = tree_types_dict

    def update_coords(self, fill_cords, grid, numerical_representation, center, env):
        plantable = True
        for coord in fill_cords:
            y, x = coord
            if grid[y][x] != 0 or env.grid[y][x].is_plantable() is False:
                plantable = False
                break
        if plantable:
            for coord in fill_cords:
                y, x = coord
                #print(coord)
                grid[y][x] = numerical_representation #change grid of surrounding tree radius to negative (occupied)
                #print("grid at: " + str(y) + " " + str(x) + " " + str(grid[y][x]))
            x, y = center
            grid[y][x] = abs(numerical_representation) #change base of tree to its positive representation
        return grid, plantable

    def remove_tree(self, fill_cords, grid, env):
        for coord in fill_cords:
            y, x = coord
            grid[y][x] = 0
            env.grid[y][x].tree = None
            env.grid[y][x].plantable = True
        return grid

    def generate_tree_radius_png(self):
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


