import copy
from Trees.TreeSpacing import TreeSpacing
from Trees.TreeGenerator import TreeGenerator
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, BoundaryNorm
random.seed(100)

class AlgorithmMutations:
    """
    Class to handle the mutations of the genetic algorithm. This class will handle verifying planting is possible,
    swapping trees and planting trees.

    :param tree_types_dict (dict): dictionary of tree type id and species
    :param env (Grid object): environment object
    """

    def __init__(self, tree_types_dict, env):
        """
        Constructor for the AlgorithmMutations class

        :param tree_types_dict (dict): dictionary of tree type id and species
        :param env (Grid object): environment object
        """
        self.tree_types_dict = tree_types_dict
        self.env = env
        self.spacing = TreeSpacing(self.tree_types_dict)
        self.generator = TreeGenerator()


    def snap_to_center(self, x, y):
        """
        Method to snap the x, y coordinates to the center of the tree. If spot is occupied by tree, this snaps to the cell
        that is occupied by the center of the tree.

        :param x (int): x coordinate
        :param y (int): y coordinate
        :return: cpprdinates of the center of the tree
        """
        if self.env.grid[y][x].tree:
            return self.env.grid[y][x].tree.getPlantingLocation()
        else:
            return None, None #no tree in position, is a plantable area


    def plant_tree(self, tree_type, x, y):
        """
        Method to plant a tree at a given x, y coordinate. Checks if tree can be planted at the location, and if not, does a local search to plant.
        If both fail, the tree is not planted.

        :param tree_type (int): tree id of the tree to plant
        :param x (int): x coordinate
        :param y (int): y coordinate
        :return: boolean if tree is plantable
        """

        tree = self.generator.generateTree(self.tree_types_dict[tree_type], (x, y)) #generate tree object
        occupied_spots, numerical_representation = tree.returnOccupiedSpots() #return occupied spots of coordinates
        numerical_grid_copy = copy.deepcopy(self.env.numerical_grid)
        numerical_grid_copy, plantable = self.spacing.update_coords(occupied_spots, numerical_grid_copy, numerical_representation, (x, y), self.env) #update grid with new tree
        self.env.numerical_grid = numerical_grid_copy

        #if not plantable, search localized grid to place tree in a plantable area
        if not plantable:
            plantable = self.local_search(tree_type, x, y)
        else:
            for spot in occupied_spots: #update the grid with the new tree object if plantable
                y, x = spot
                self.env.plant(x, y, tree)
        return plantable

    def overlay_tree(self, tree_type, x, y):
        """
        Method to overlay a tree on top of another tree. If the new tree does not fit, the old tree is reverted back to its original position.

        :param tree_type (int): tree id of the tree to plant
        :param x (int): x coordinate
        :param y (int): y coordinate
        """
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
            if not plantable: #if new tree does not fit, revert back to old tree
                self.env.numerical_grid = temp_grid
        else: #no tree in position, just plant new tree
            self.plant_tree(tree_type, x, y)

    def swap_trees(self, x1, y1, x2, y2):
        """
        Method to swap two trees in the environment. If one of the spots is empty, the tree is moved to the empty spot.
        If both spots are empty, nothing happens.

        :param x1 (int): x coordinate of first tree
        :param y1 (int): y coordinate of first tree
        :param x2 (int): x coordinate of second tree
        :param y2 (int): y coordinate of second tree
        """
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
        """
        Method to search in a 5x5 grid around the current position to find a plantable area. If found, plant the tree. Otherwise,
        no tree is planted.

        :param tree_type (int): tree id of the tree to plant
        :param curr_x (int): x coordinate about which is center of local search
        :param curr_y (int): y coordinate about which is center of local search
        :return: boolean plantable
        """

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