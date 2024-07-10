
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

    def __init__(self, x, y, by_road, plantable, hedge, big_tree_area, pedestrian_road):
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
        self.road = by_road
        self.plantable = plantable
        self.hedge = hedge
        self.big_tree_area = big_tree_area
        self.pedestrian_road = pedestrian_road

    def get_coordinates(self):
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

    def check_near_squares(self, radius):
        """
        Returns true or false if a square can be planted on by checking if near squares have trees planted on them.
        :param radius: radius to check for near squares
        :return:
        """

        pass

    def by_road(self):
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

    def tree_obj(self):
        return self.tree

    def is_hedge(self):
        """
        Method to check if a square is a hedge
        :return: true if square is a hedge, false otherwise
        """
        return self.hedge

    def is_big_tree_area(self):
        """
        Method to check if a square is a big tree area
        :return: true if square is a big tree area, false otherwise
        """
        return self.big_tree_area

    def is_pedestrian_road(self):
        """
        Method to check if a square is a pedestrian road
        :return: true if square is a pedestrian road, false otherwise
        """
        return self.pedestrian_road

    def get_numeric_representation(self):
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