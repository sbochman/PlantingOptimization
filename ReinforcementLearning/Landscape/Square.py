
class Square:
    """
    Square class which represents a 1-meter by 1-meter square in a grid. The grid is a 2D array of squares that
    resembles the environment.

    Attributes:
        x: x-coordinate of the square
        y: y-coordinate of the square
        tree: tree object planted on the square
        road: boolean to check if the square is by a road
    """

    def __init__(self, x, y, byRoad, plantable):
        """
        Constructor for the Square class
        :param x: x coordinate in grid
        :param y: y coordinate in grid
        :param byRoad: boolean to check if square is by a road
        :param plantable: boolean to check if square is plantable
        """
        self.x = x
        self.y = y
        self.tree = None
        self.road = byRoad
        self.plantable = plantable

    def getCoordinates(self):
        """
        Method to get the coordinates of a square
        :return: tuple of x and y coordinates
        """
        return self.x, self.y

    def plant(self, tree):
        """
        Method to plant a tree on a square
        :return: true if tree is planted, false otherwise
        """
        if self.plantable:
            self.tree = tree
            self.plantable = False
        else: return False

    def checkNearSquares(self, radius):
        """
        Returns true or false if a square can be planted on by checking if near squares have trees planted on them.
        :param radius: radius to check for near squares
        :return:
        """

        pass

    def byRoad(self):
        """
        Method to check if a square is by a road
        :return: true if square is by a road, false otherwise
        """
        return self.road

    def plantable(self):
        """
        Method to check if a square is plantable
        :return: true if square is plantable, false otherwise
        """
        if self.plantable:
            return True
        return False

    def treeObj(self):
        return self.tree

    def getNumericRepresentation(self):
        """
        Method to get the numeric representation of the square
        :return: the numeric representation of the square
        """
        if self.tree:
            if self.tree.numericalRepresentation == 0: return -2
            return self.tree.numericalRepresentation
        elif not self.plantable:
            return -1
        else:
            return 0