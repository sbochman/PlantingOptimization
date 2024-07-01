"""
Class to specify the methods that a tree should have. There are 21 tree species
in the dataset, and each tree has a specific set of attributes. Each species will be a
subclass of this abstract class.
"""
class Tree:

    def __init__(self, leafType, plantingLocation, plantSize, species, creditValue, crownArea, co2Absorption, price, treeCategory, numericalRepresentation):
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
        self.leafType = leafType
        self.plantingLocation = plantingLocation
        self.plantSize = plantSize
        self.species = species
        self.creditValue = creditValue
        self.crownArea = crownArea
        self.co2Absorption = co2Absorption
        self.price = price
        self.treeCategory = treeCategory
        self.numericalRepresentation = numericalRepresentation

    def getLeafType(self):
        """
        Method to get the type of leaf the tree has
        :return: type of leaf the tree has
        """
        return self.leafType

    def getPlantingLocation(self):
        """
        Method to get the location where the tree is planted
        :return: (x, y) coordinates of the location where tree is planted
        """
        return self.plantingLocation

    def getPlantSize(self):
        """
        Method to get the size of the tree
        :return: the size of the tree
        """
        return self.plantSize

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
        return self.creditValue

    def getCrownArea(self):
        """
        Method to get the area of the crown
        :return: area of the crown
        """
        return self.crownArea

    def getCo2Absorption(self):
        """
        Method to get the amount of CO2 absorbed by the tree
        :return: CO2 absorbed by the tree
        """
        return self.co2Absorption

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
        return self.treeCategory

    def getNumericalRepresentation(self):
        """
        Method to get the numerical representation of the tree
        :return: numerical representation of the tree
        """
        return self.numericalRepresentation