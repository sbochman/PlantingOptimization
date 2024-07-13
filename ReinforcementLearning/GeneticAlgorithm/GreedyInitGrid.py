import random
random.seed(100)

class GreedyInitGrid:

    def __init__(self, x, y, individual, tree_types_dict, generator, fitness_eval, mutations):
        self.x = x
        self.y = y
        self.individual = individual
        self.tree_types_dict = tree_types_dict
        self.generator = generator
        self.constraints = fitness_eval
        self.mutations = mutations
        self.violations =  {"min_trees_to_landscape": [1, 2, 7, 19, 20, 21],
                            "min_evergreen_to_all": [1, 2, 3, 4, 5, 6],
                            "min_native_to_all": [13, 20],
                            "min_large_to_all": [2, 3, 7, 21],
                            "max_canopy_coverage": [0],
                            "min_canopy_coverage": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                            "min_evergreen_count": [1, 2, 3, 4, 5, 6],
                            "min_deciduous_count": [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21],
                            "total_cost": [0]
                           }
        self.areas =  {"hedge": [1, 6],
                       "big_tree_area": [2, 3, 7, 21],
                       "plantable": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21]
                      }


    def init_grid(self):
        #must populate hedge with screening trees, so plant trees in hedge areas first

        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].hedge:
                    tree_type = random.choice(self.areas["hedge"])
                    self.mutations.plant_tree(tree_type, j, i)

        #populate big tree areas with large trees
        for i in range(self.y):
            for j in range(self.x):
                if self.individual.grid.grid[i][j].big_tree_area:
                    #random chance to plant a tree in big tree area
                    chance = random.choice([1, 2, 3, 4, 5])
                    if chance < 3: continue #random chance to not plant tree
                    tree_type = random.choice(self.areas["big_tree_area"])
                    self.mutations.plant_tree(tree_type, j, i)

        for i in range(self.y):
            for j in range(self.x):
                #check fitness_eval to see what constraint is being violated
                if self.individual.grid.grid[i][j].plantable:
                    #which constraint is being violated?
                    flatten_grid = self.individual.grid.numerical_grid.flatten()
                    constraint = self.constraints.validate(flatten_grid)
                    if constraint == None: return self.individual #all constraints are met return and use initial grid for genetic algorithm
                    tree_type = random.choice(self.violations[constraint])
                    self.mutations.plant_tree(tree_type, j, i)
                else:
                    pass
        #print('not satisfied with constraints, try again')
        return None #not satisfied with constraints, try again



