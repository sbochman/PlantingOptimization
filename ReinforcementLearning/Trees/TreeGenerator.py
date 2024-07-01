from Trees.Tree import Tree

class SingletonMeta(type):
    """
    Singleton metaclass to ensure that only one instance of the TreeGenerator class is created
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class TreeGenerator(metaclass=SingletonMeta):
    """
    Class to generate trees. Several functions to generate trees are defined here. The input is only the (x, y)
    coordinates of the location where the tree is planted. The function name is the species to generate.
    """

    def __init__(self):
        """
        Constructor for the TreeGenerator class
        """
        pass

    def generateTree(self, species, plantingLocation):
        """
        Method to generate trees
        :param species: species of the tree
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        if species == "Abies Holophylla":
            return self.abiesHolophylla(plantingLocation)
        elif species == "Pinus Desniflora1":
            return self.pinusDesniflora1(plantingLocation)
        elif species == "Pinus Desniflora2":
            return self.pinusDesniflora2(plantingLocation)
        elif species == "Pinus Desniflora Globosa":
            return self.pinusDesnifloraGlobosa(plantingLocation)
        elif species == "Taxus Cuspidata":
            return self.taxusCuspidata(plantingLocation)
        elif species == "White Pine":
            return self.whitePine(plantingLocation)
        elif species == "Acer Palmatum":
            return self.acerPalmatum(plantingLocation)
        elif species == "Betula Platyphylla":
            return self.betulaPlatyphylla(plantingLocation)
        elif species == "Cercidiphyllum Japonicum":
            return self.cercidiphyllumJaponicum(plantingLocation)
        elif species == "Chaenomeless Sinensis":
            return self.chaenomelessSinensis(plantingLocation)
        elif species == "Chionanthus Retusus":
            return self.chionanthusRetusus(plantingLocation)
        elif species == "Cornus Officinalis":
            return self.cornusOfficinalis(plantingLocation)
        elif species == "Ginkgo Biloba":
            return self.ginkgoBiloba(plantingLocation)
        elif species == "Kobus Magnolia":
            return self.kobusMagnolia(plantingLocation)
        elif species == "Liriodendron Tulipifera":
            return self.liriodendronTulipifera(plantingLocation)
        elif species == "Oak":
            return self.oak(plantingLocation)
        elif species == "Persimmon":
            return self.persimmon(plantingLocation)
        elif species == "Prunus Armeniaca":
            return self.prunusArmeniaca(plantingLocation)
        elif species == "Prunus Yedoensis":
            return self.prunusYedoensis(plantingLocation)
        elif species == "Sophora Japonica":
            return self.sophoraJaponica(plantingLocation)
        elif species == "Zelkova Serrata":
            return self.zelkovaSerrata(plantingLocation)
        elif species == "None":
            return self.none(plantingLocation)

    def abiesHolophylla(self, plantingLocation):
        """
        Method to generate Abies Holophylla trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Evergreen", plantingLocation, (3.0, 1.5, 7.0), "Abies Holphylla",1, 1.8, 2.2, 135, "Screen", 1)

    def pinusDesniflora1(self, plantingLocation):
        """
        Method to generate Pinus Desniflora trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Evergreen", plantingLocation, (8.0, 5.6, 25.0), "Pinus Desniflora1", 4, 24.6, 5.4, 1949, "Large", 2)

    def pinusDesniflora2(self, plantingLocation):
        """
        Method to generate Pinus Desniflora trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Evergreen", plantingLocation, (8.0, 5.6, 30.0), "Pinus Desniflora2", 4, 24.6, 5.4, 2881, "Large", 3)

    def pinusDesnifloraGlobosa(self, plantingLocation):
        """
        Method to generate Pinus Desniflora trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Evergreen", plantingLocation, (2.0, 2.5, 15.0), "Pinus Desniflora Globosa", 1, 4.9, 5.4, 1398, "None", 4)

    def taxusCuspidata(self, plantingLocation):
        """
        Method to generate Taxus Cuspidata trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Evergreen", plantingLocation, (3.0, 2.0, 7.0), "Taxus Cuspidata", 1, 3.1, 0.5, 1864, "None", 5)

    def whitePine(self, plantingLocation):
        """
        Method to generate White Pine trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Evergreen", plantingLocation, (3.0, 1.5, 8.0), "White Pine", 1, 3.1, 3.8, 57, "Screen", 6)

    def acerPalmatum(self, plantingLocation):
        """
        Method to generate Acer Palmatum trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.0, 2.8, 20.0), "Acer Palmatum", 4, 6.2, 3.1, 796, "Large", 7)

    def betulaPlatyphylla(self, plantingLocation):
        """
        Method to generate Betula Platyphylla trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (5.0, 3.5, 12.0), "Betula Platyphylla", 1, 9.6, 3.8, 279, "None", 8)

    def cercidiphyllumJaponicum(self, plantingLocation):
        """
        Method to generate Cercidiphyllum Japonicum trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.5, 3.2, 15.0), "Cercidiphyllum Japonicum", 2, 8.0, 3.8, 423, "None", 9)

    def chaenomelessSinensis(self, plantingLocation):
        """
        Method to generate Chaenomeless Sinensis trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.0, 2.8, 15.0), "Chaenomeless Sinensis", 2, 6.2, 3.8, 381, "None", 10)

    def chionanthusRetusus(self, plantingLocation):
        """
        Method to generate Chionanthus Retusus trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.0, 2.8, 15.0), "Chionanthus Retusus", 2, 6.2, 3.5, 550, "None", 11)

    def cornusOfficinalis(self, plantingLocation):
        """
        Method to generate Cornus Officinalis trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (3.0, 1.5, 10.0), "Cornus Officinalis", 1, 1.8, 2.9, 211, "None", 12)

    def ginkgoBiloba(self, plantingLocation):
        """
        Method to generate Ginkgo Biloba trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (5.0, 3.5, 15.0), "Ginkgo Biloba", 2, 9.6, 4.5, 406, "Native", 13)

    def kobusMagnolia(self, plantingLocation):
        """
        Method to generate Kobus Magnolia trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (3.5, 3.5, 15.0), "Kobus Magnolia", 2,  9.6, 3.8, 423, "None", 14)

    def liriodendronTulipifera(self, plantingLocation):
        """
        Method to generate Liriodendron Tulipifera trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (5.0, 3.5, 15.0), "Liriodendron Tulipifera", 2, 9.6, 3.8, 389, "None", 15)

    def oak(self, plantingLocation):
        """
        Method to generate Oak trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.0, 2.8, 15.0), "Oak", 2, 6.2, 3.8, 423, "None", 16)

    def persimmon(self, plantingLocation):
        """
        Method to generate Persimmon trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (3.5, 2.5, 12.0), "Persimmon", 1, 4.9, 3.8, 186, "None", 17)

    def prunusArmeniaca(self, plantingLocation):
        """
        Method to generate Prunus Armeniaca trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (2.5, 1.8, 6.0), "Prunus Armeniaca", 1, 2.5, 3.8, 55, "None", 18)

    def prunusYedoensis(self, plantingLocation):
        """
        Method to generate Prunus Yedoensis trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.5, 3.2, 15.0), "Prunus Yedoensis", 2, 8.0, 9.0, 576, "None", 19)

    def sophoraJaponica(self, plantingLocation):
        """
        Method to generate Sophora Japonica trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (4.5, 3.2, 15.0), "Sophora Japonica", 2, 8.0, 3.8, 322, "Native", 20)

    def zelkovaSerrata(self, plantingLocation):
        """
        Method to generate Zelkova Serrata trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("Deciduous", plantingLocation, (5.0, 3.5, 30.0), "Zelkova Serrata", 4, 9.6, 14.8, 1949, "Large", 21)

    def none(self, plantingLocation):
        """
        Method to generate trees
        :param plantingLocation: (x, y) coordinates of the location where tree is planted
        :return: Tree object
        """
        return Tree("", plantingLocation, (0, 0, 0), "None", 0, 0, 0, 0, "", 0)