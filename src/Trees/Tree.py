import math

class Tree:
    """
    Class to represent a tree. Each tree has a leaf type, planting location, plant size, species, credit value, crown area,
    CO2 absorption, price, tree category, and numerical representation. This Tree object is planted in the Grid object Square class.

    Attributes:
        leaf_type (string): String type of leaf the tree has
        planting_location (int, int): (x, y) coordinates of the location where tree is planted
        plant_size (float, float, float): tuple of Floats (x, y, z) size of the tree where x is height, y is width, and z is diamoter of root
        species (string): String species of the tree
        credit_value (int): Integer credit value of the tree
        crown_area (float): Float area of the crown
        co2_absorption (float): Float amount of CO2 absorbed
        price (int): Integer price of the tree
        tree_category (string): String category of the tree being either screening, large, or native.
        numerical_representation (int): Integer numerical representation of the tree
    """
    def __init__(self, leaf_type, planting_location, plant_size, species, credit_value, crown_area, co2_absorption, price, tree_category, numerical_representation):
        """
        Constructor for the Tree class

        :param leaf_type (string): String type of leaf the tree has
        :param planting_location (int, int): (x, y) coordinates of the location where tree is planted
        :param plant_size (float, float, float): tuple of Floats (x, y, z) size of the tree where x is height, y is width, and z is diamoter of root
        :param species (string): String species of the tree
        :param credit_value (int): Integer credit value of the tree
        :param crown_area (float): Float area of the crown
        :param co2_absorption (float): Float amount of CO2 absorbed
        :param price (int): Integer price of the tree
        :param tree_category (string): String category of the tree being either screening, large, or native.
        :param numerical_representation (int): Integer numerical representation of the tree
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
        #self.fillGridRadius(202, 121)

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
        """
        Method to return the occupied spots by the tree

        :return: the occupied spots by the tree
        """
        return self.occupied, -1 * self.getNumericalRepresentation()

