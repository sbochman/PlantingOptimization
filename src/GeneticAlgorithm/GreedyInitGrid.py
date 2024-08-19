import random
random.seed(100)

class GreedyInitGrid:
    """
    GreedyInitGrid class is responsible for initializing the grid with trees in a greedy manner. The class is used to populate the intial population of the genetic algorithm.

    Attributes:
        x (int): x-coordinate of the grid
        y (int): y-coordinate of the grid
        individual (Individual): individual object to be populated
        tree_types_dict (dict): dictionary of tree type ID and species
        generator (TreeGenerator): tree generator object to generate trees
        fitness_eval (Constraint): fitness evaluation object
        mutations (AlgorithmMutations): mutations object
    """
    def __init__(self, x, y, individual, tree_types_dict, generator, fitness_eval, mutations):
        """
        Constructor for the GreedyInitGrid class.

        :param x (int): x-coordinate of the grid
        :param y (int): y-coordinate of the grid
        :param individual (Individual): individual object to be populated
        :param tree_types_dict (dict): dictionary of tree type ID and species
        :param generator (TreeGenerator): tree generator object to generate trees
        :param fitness_eval (Constraint): fitness evaluation object
        :param mutations (AlgorithmMutations): mutations object
        """
        self.x = x
        self.y = y
        self.individual = individual
        self.tree_types_dict = tree_types_dict
        self.generator = generator
        self.constraints = fitness_eval
        self.mutations = mutations
        #define trees to plant given constraint violated. These trees help to satisfy the constraint.
        self.violations_apartment =  {"min_trees_to_landscape": [1, 4, 6, 7, 21],
                            "min_evergreen_to_all": [1, 2, 3, 4, 5, 6],
                            "min_native_to_all": [13, 20],
                            "min_large_to_all": [2, 3, 7, 21],
                            "max_canopy_coverage": [0],
                            "min_canopy_coverage": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                            "min_evergreen_count": [1, 2, 3, 4, 5, 6],
                            "min_deciduous_count": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                            "pedestrian_road_planting": [1, 2, 3, 4, 5, 6, 7, 21],
                            "hedge_planting": [1, 6],
                            "total_cost": [0]
                           }
        self.areas =  {"hedge": [1, 6],
                       "big_tree_area": [2, 3, 7, 21],
                       "plantable": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                       "native": [13, 20]
                      }

        self.violations_park = {"min_trees_to_landscape": [1, 7, 20, 21],
                                "min_evergreen_to_all": [1, 5, 6],
                                "min_large_to_all": [7, 21],
                                "min_native_to_all": [13, 20],
                                "max_canopy_coverage": [0],
                                "min_canopy_coverage": [1, 5, 6, 7, 8, 9, 11, 13, 14, 15, 16, 17, 18,  20, 21],
                                "min_evergreen_count": [1, 2, 3, 4, 5, 6],
                                "min_deciduous_count": [7, 8, 9, 11, 13, 14, 15, 16, 17, 18, 20, 21],
                                "total_cost": [0],
                                "too_many_trees": [0]
                                }

    def init_grid_scenario_one(self):
        """
        Method to initialize the grid with trees for scenario one. This is a greedy algorithm that populates the grid with trees based on the constraints violated.
        If a constraint is violated, the algorithm will plant trees that help to satisfy the constraint.

        :return (Individual): individual object with populated grid
        """
        #must populate hedge with screening trees, so plant trees in hedge areas first

        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].hedge:
                    chance = random.randint(1, 25)
                    if i < 350 and chance < 3:
                        tree_type = random.choice(self.areas["hedge"])
                        self.mutations.plant_tree(tree_type, j, i)
                    elif i > 350:
                        tree_type = random.choice(self.areas["hedge"])
                        self.mutations.plant_tree(tree_type, j, i)

        #populate road areas with trees. set interval to 2 meters - meaning set additional 4 blocks up, down, left, right to be unplantable
        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].pedestrian_road:
                    chance = random.randint(1, 10)
                    if i < 322 and chance < 4:
                        tree_type = random.choice(self.areas["plantable"])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        tree_type = random.choice(self.areas["plantable"])
                        self.mutations.plant_tree(tree_type, j, i)


        #populate road areas with trees. set interval to 2 meters - meaning set additional 4 blocks up, down, left, right to be unplantable
        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].road:
                    #tree should flip back and forth between tree 13 and 20 to plant for aesthetic purposes
                    chance = random.randint(1, 25)
                    if chance < 3:
                        tree_type = self.areas["native"][i % 2]
                        self.mutations.plant_tree(tree_type, j, i)

        #populate big tree areas with large trees
        for i in range(self.y):
            for j in range(self.x):
                chance = random.randint(1, 30)
                if chance < 2:
                    if self.individual.grid.grid[i][j].big_tree_area:
                        #random chance to plant a tree in big tree area
                        chance = random.choice([1, 2, 3, 4, 5, 6, 7])
                        if chance < 3: continue #random chance to not plant tree
                        tree_type = random.choice(self.areas["big_tree_area"])
                        self.mutations.plant_tree(tree_type, j, i)

        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].pedestrian_road:
                    constraint = self.constraints.validate(self.individual.grid.numerical_grid.flatten())
                    if constraint == None: return self.individual #all constraints are met return and use initial grid for genetic algorithm
                    if constraint == "pedestrian_road_planting":
                        tree_type = random.choice([1, 2, 3, 4, 5, 6, 7, 21])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        tree_type = random.choice(self.violations_apartment[constraint])
                        self.mutations.plant_tree(tree_type, j, i)
                chance = random.randint(1, 40)
                if chance < 2:
                    #check fitness_eval to see what constraint is being violated
                    if self.individual.grid.grid[i][j].plantable:
                        #which constraint is being violated?
                        flatten_grid = self.individual.grid.numerical_grid.flatten()
                        constraint = self.constraints.validate(flatten_grid)
                        if constraint == None: return self.individual #all constraints are met return and use initial grid for genetic algorithm
                        tree_type = random.choice(self.violations_apartment[constraint])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        pass
        return None #not satisfied with constraints, try again


    def init_grid_scenario_two(self):
        """
        Method to initialize the grid with trees for scenario two. This is a greedy algorithm that populates the grid with trees based on the constraints violated.
        If a constraint is violated, the algorithm will plant trees that help to satisfy the constraint.

        :return: Individual object with populated grid
        """
        #must populate hedge with screening trees, so plant trees in hedge areas first

        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].hedge:
                    chance = random.randint(1, 25)
                    if i < 350 and chance < 3:
                        tree_type = random.choice(self.areas["hedge"])
                        self.mutations.plant_tree(tree_type, j, i)
                    elif i > 350:
                        tree_type = random.choice(self.areas["hedge"])
                        self.mutations.plant_tree(tree_type, j, i)

        #populate road areas with trees. set interval to 2 meters - meaning set additional 4 blocks up, down, left, right to be unplantable
        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].pedestrian_road:
                    chance = random.randint(1, 10)
                    if i < 322 and chance < 4:
                        tree_type = random.choice(self.areas["plantable"])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        tree_type = random.choice(self.areas["plantable"])
                        self.mutations.plant_tree(tree_type, j, i)


        #populate road areas with trees. set interval to 2 meters - meaning set additional 4 blocks up, down, left, right to be unplantable
        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].road:
                    #tree should flip back and forth between tree 13 and 20 to plant for aesthetic purposes
                    chance = random.randint(1, 25)
                    if chance < 3:
                        tree_type = self.areas["native"][i % 2]
                        self.mutations.plant_tree(tree_type, j, i)

        #populate big tree areas with large trees
        for i in range(self.y):
            for j in range(self.x):
                chance = random.randint(1, 30)
                if chance < 2:
                    if self.individual.grid.grid[i][j].big_tree_area:
                        #random chance to plant a tree in big tree area
                        chance = random.choice([1, 2, 3, 4, 5, 6, 7])
                        if chance < 3: continue #random chance to not plant tree
                        tree_type = random.choice(self.areas["big_tree_area"])
                        self.mutations.plant_tree(tree_type, j, i)

        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].pedestrian_road:
                    constraint = self.constraints.validate(self.individual.grid.numerical_grid.flatten())
                    if constraint == None: return self.individual #all constraints are met return and use initial grid for genetic algorithm
                    if constraint == "pedestrian_road_planting":
                        tree_type = random.choice([1, 2, 3, 4, 5, 6, 7, 21])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        tree_type = random.choice(self.violations_apartment[constraint])
                        self.mutations.plant_tree(tree_type, j, i)
                chance = random.randint(1, 40)
                if chance < 2:
                    #check fitness_eval to see what constraint is being violated
                    if self.individual.grid.grid[i][j].plantable:
                        #which constraint is being violated?
                        flatten_grid = self.individual.grid.numerical_grid.flatten()
                        constraint = self.constraints.validate(flatten_grid)
                        if constraint == None: return self.individual #all constraints are met return and use initial grid for genetic algorithm
                        tree_type = random.choice(self.violations_apartment[constraint])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        pass
        return None #not satisfied with constraints, try again

    def init_grid_edinburgh(self):
        """
        Method to initialize the grid with trees for scenario three. This is a greedy algorithm that populates the grid with trees based on the constraints violated.
        If a constraint is violated, the algorithm will plant trees that help to satisfy the constraint.

        :return: Individual object with populated grid
        """
        for i in range(self.y):
            for j in range(self.x):
                #random chance to plot a tree
                chance = random.randint(1, 1000)
                if chance < 4:
                    #check fitness_eval to see what constraint is being violated
                    if self.individual.grid.grid[i][j].plantable:
                        #which constraint is being violated?
                        flatten_grid = self.individual.grid.numerical_grid.flatten()
                        constraint = self.constraints.validate(flatten_grid)
                        if constraint == None:
                            return self.individual #all constraints are met return and use initial grid for genetic algorithm
                        tree_type = random.choice(self.violations_park[constraint])
                        self.mutations.plant_tree(tree_type, j, i)
                    else:
                        pass
        return None #not satisfied with constraints, try again

