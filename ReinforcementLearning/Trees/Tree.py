import math
import numpy as np
"""
Class to specify the methods that a tree should have. There are 21 tree species
in the dataset, and each tree has a specific set of attributes. Each species will be a
subclass of this abstract class.
"""
class Tree:

    def __init__(self, leaf_type, planting_location, plant_size, species, credit_value, crown_area, co2_absorption, price, tree_category, numerical_representation):
        """
        Constructor for the Tree class
        :param leafType: String type of leaf the tree has
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :param plantSize: tuple of Floats (x, y, z) size of the tree where x is height, y is width, and z is diamoter of root
        :param species: String species of the tree
        :param creditValue: Integer credit value of the tree
        :param crownArea: Float area of the crown
        :param co2Absorption: Float amount of CO2 absorbed
        :param price: Integer price of the tree
        :param treeCategory: String category of the tree being either screening, large, or native.
        :param numericalRepresentation: Integer numerical representation of the tree
        """
        self.leaf_type = leaf_type
        self.planting_location = planting_location
        self.plant_size = plant_size
        self.species = species
        self.credit_value = credit_value
        self.crown_area = crown_area
        self.co2_absorption = co2_absorption
        self.price = price
        self.tree_category = tree_category
        self.numerical_representation = numerical_representation
        self.occupied = []
        self.fillGridRadius(335, 514) #change to actual height

    def getLeafType(self):
        """
        Method to get the type of leaf the tree has
        :return: type of leaf the tree has
        """
        return self.leaf_type

    def getPlantingLocation(self):
        """
        Method to get the location where the tree is planted
        :return: (x, y) coordinates of the location where tree is planted
        """
        return self.planting_location

    def getPlantSize(self):
        """
        Method to get the size of the tree
        :return: the size of the tree
        """
        return self.plant_size

    def getSpecies(self):
        """
        Method to get the species of the tree
        :return: species of the tree
        """
        return self.species

    def getCreditValue(self):
        """
        Method to get the credit value of the tree
        :return: credit value of the tree
        """
        return self.credit_value

    def getCrownArea(self):
        """
        Method to get the area of the crown
        :return: area of the crown
        """
        return self.crown_area

    def getCo2Absorption(self):
        """
        Method to get the amount of CO2 absorbed by the tree
        :return: CO2 absorbed by the tree
        """
        return self.co2_absorption

    def getPrice(self):
        """
        Method to get the price of the tree
        :return: price of the tree
        """
        return self.price

    def getTreeCategory(self):
        """
        Method to get the category of the tree
        :return: category of the tree
        """
        return self.tree_category

    def getNumericalRepresentation(self):
        """
        Method to get the numerical representation of the tree
        :return: numerical representation of the tree
        """
        return self.numerical_representation

    def fillGridRadius(self, grid_width, grid_height):
        """
        Method to fill the grid with the tree's radius. only take a subset of the total
        grid space to improve on time complexity
        :return: the grid with the tree's radius
        """

        radius = math.ceil(self.getPlantSize()[1] / 2) #each cell is 0.5 meters so / 2 instead of 4
        center_x, center_y = self.getPlantingLocation()
        min_x = max(0, center_x - radius)
        max_x = min(grid_width - 1, center_x + radius)
        min_y = max(0, center_y - radius)
        max_y = min(grid_height - 1, center_y + radius)

        for i in range(min_y, max_y + 1):
            for j in range(min_x, max_x + 1):
                if (i - center_y)**2 + (j - center_x)**2 <= radius**2:
                    self.occupied.append([i, j]) # to represent type of tree and area occupied by that tree print -1 * numerical_representation

    def returnOccupiedSpots(self):
        return self.occupied, -1 * self.getNumericalRepresentation()

