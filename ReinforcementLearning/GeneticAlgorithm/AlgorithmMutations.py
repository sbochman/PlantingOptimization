import copy
from Trees.TreeSpacing import TreeSpacing
from Trees.TreeGenerator import TreeGenerator
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
random.seed(100)

class AlgorithmMutations:
    def __init__(self, tree_types_dict, env):
        self.tree_types_dict = tree_types_dict
        self.env = env
        self.spacing = TreeSpacing(self.tree_types_dict)
        self.generator = TreeGenerator()


    def snap_to_center(self, x, y):
        if self.env.grid[y][x].tree:
            return self.env.grid[y][x].tree.getPlantingLocation()
        else:
            return None, None #no tree in position, is a plantable area


    def plant_tree(self, tree_type, x, y):
        tree = self.generator.generateTree(self.tree_types_dict[tree_type], (x, y))
        occupied_spots, numerical_representation = tree.returnOccupiedSpots()
        numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
        numerical_grid_copy, plantable = self.spacing.update_coords(occupied_spots, numerical_grid_copy, numerical_representation, (x, y), self.env)
        self.env.numerical_grid = numerical_grid_copy
        #if not plantable, search localized grid to place tree in a plantable area
        if not plantable:
            plantable = self.local_search(tree_type, x, y)
        else:
            for spot in occupied_spots: #update the grid with the new tree object if plantable
                y, x = spot
                self.env.plant(x, y, tree)
        return plantable
            #print('planting tree at: ' + str(x) + ', ' + str(y) + ' with type: ' + str(tree_type))

    def overlay_tree(self, tree_type, x, y):
        #find old tree object in position
        old_x, old_y = self.snap_to_center(x, y)
        if old_x is not None: #if there is a tree in position
            old_tree = self.env.grid[old_y][old_x].tree
            #create temp grid copy to revert back to if new tree does not fit
            temp_grid = copy.deepcopy(self.env.numerical_grid)
            #take occupied spots and turn to 0
            occupied_spots, numerical_representation = old_tree.returnOccupiedSpots()
            numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
            numerical_grid_copy = self.spacing.remove_tree(occupied_spots, numerical_grid_copy, self.env)
            self.env.numerical_grid = numerical_grid_copy

            #now overlay new tree
            plantable = self.plant_tree(tree_type, x, y)
            #tree = self.generator.generateTree(self.tree_types_dict[tree_type], (x, y))
            #occupied_spots, numerical_representation = tree.returnOccupiedSpots()
            #numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
            #numerical_grid_copy, plantable = self.spacing.update_coords(occupied_spots, numerical_grid_copy, numerical_representation, tree.getPlantingLocation(), self.env)
            #self.env.numerical_grid = numerical_grid_copy
            if not plantable: #if new tree does not fit, revert back to old tree
                self.env.numerical_grid = temp_grid
            #else:
             #   for spot in occupied_spots:
              #      y, x = spot
               #     self.env.plant(x, y, tree)
        else: #no tree in position, just plant new tree
            self.plant_tree(tree_type, x, y)

    def swap_trees(self, x1, y1, x2, y2):
        #save current grid if swap is not possible
        original_temp_grid = copy.deepcopy(self.env.numerical_grid)

        #if x1, y1 and x2, y2 is a tree, save the tree object
        tree1 = self.env.grid[y1][x1].tree
        tree2 = self.env.grid[y2][x2].tree

        #swap tree2 to tree1 position using overlay_tree
        if tree1 and not tree2:
            #now remove old tree position
            numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
            numerical_grid_copy = self.spacing.remove_tree(tree1.returnOccupiedSpots()[0], numerical_grid_copy, self.env)
            self.env.numerical_grid = numerical_grid_copy
            #now plant
            self.overlay_tree(tree1.getNumericalRepresentation(), x2, y2)

        elif tree2 and not tree1:
            #now remove old tree position
            numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
            numerical_grid_copy = self.spacing.remove_tree(tree2.returnOccupiedSpots()[0], numerical_grid_copy, self.env)
            self.env.numerical_grid = numerical_grid_copy
            #now plant
            self.overlay_tree(tree2.getNumericalRepresentation(), x1, y1)

        elif tree1 and tree2: #can try and swap both trees as both exist
            #remove both trees
            numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
            numerical_grid_copy = self.spacing.remove_tree(tree1.returnOccupiedSpots()[0], numerical_grid_copy, self.env)
            numerical_grid_copy = self.spacing.remove_tree(tree2.returnOccupiedSpots()[0], numerical_grid_copy, self.env)
            self.env.numerical_grid = numerical_grid_copy

            self.overlay_tree(tree1.getNumericalRepresentation(), x2, y2)
            self.overlay_tree(tree2.getNumericalRepresentation(), x1, y1)

        else: #neither spot contains a tree
            pass


    def local_search(self, tree_type, curr_x, curr_y):
        #search in a 4x4 grid around the current position. handle edge cases where the search goes out of bounds
        min_x = max(0, curr_x - 2)
        max_x = min(self.env.x, curr_x + 2)
        min_y = max(0, curr_y - 2)
        max_y = min(self.env.y, curr_y + 2)
        for y in range(min_y, max_y):
            for x in range(min_x, max_x):
                if x == curr_x and y == curr_y: continue
                else:
                    #try and plant tree in position
                    tree = self.generator.generateTree(self.tree_types_dict[tree_type], (x, y))
                    occupied_spots, numerical_representation = tree.returnOccupiedSpots()
                    numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
                    numerical_grid_copy, plantable = self.spacing.update_coords(occupied_spots, numerical_grid_copy, numerical_representation, (x, y), self.env)
                    self.env.numerical_grid = numerical_grid_copy
                    if plantable:
                        for spot in occupied_spots:
                            y, x = spot
                            self.env.plant(x, y, tree)
                        return True
        return False


    def init_grid(self):
        #loop through grid and try at each location to plant a random tree
        for y in range(self.env.y):
            for x in range(self.env.x):
                #choose a random val between 0 and 22
                chance = random.choice([1, 2, 3, 4, 5])
                if chance < 4: continue
                val = random.randint(0, 21)
                tree = self.generator.generateTree(self.tree_types_dict[val], (x, y))
                #check if tree can be planted at location
                occupied_spots, numerical_representation = tree.returnOccupiedSpots()
                print('occupied_spots for tree at ' + str(x) + ', ' + str(y) + ': ' + str(occupied_spots))
                numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
                numerical_grid_copy, plantable = self.spacing.update_coords(occupied_spots, numerical_grid_copy, numerical_representation, (x, y))
                self.env.numerical_grid = numerical_grid_copy
        #print the numerical grid
        self.env.print_grid()


    def visualize_grid(self):
        printable_grid = np.zeros((self.env.y, self.env.x))
        for y in range(self.env.y):
            for x in range(self.env.x):
                if self.env.numerical_grid[y][x] < 0:
                    printable_grid[y][x] = -1
                elif self.env.numerical_grid[y][x] == 0:
                    printable_grid[y][x] = 0
                else:
                    printable_grid[y][x] = 1

        #visualize grid
        cmap = ListedColormap(['green', 'white', 'brown'])

        # Define the boundaries
        bounds = [-1.5, -0.5, 0.5, 1.5]

        # Create the norm using BoundaryNorm
        norm = BoundaryNorm(bounds, cmap.N)

        # Create the plot
        plt.figure(figsize=(9, 9))
        plt.imshow(printable_grid, cmap=cmap, norm=norm, aspect='equal')

        # Add grid lines with correct alignment
        plt.grid(True, which='both', color='black', linestyle='-', linewidth=2)
        plt.xticks(np.arange(-0.5, len(printable_grid[0]), 1), [])
        plt.yticks(np.arange(-0.5, len(printable_grid), 1), [])

        # Setting grid lines for minor ticks to ensure they are in between cells
        plt.gca().set_xticks(np.arange(-0.5, len(printable_grid[0]), 1), minor=True)
        plt.gca().set_yticks(np.arange(-0.5, len(printable_grid), 1), minor=True)
        plt.grid(True, which='minor', color='black', linestyle='-', linewidth=2)
        plt.show()