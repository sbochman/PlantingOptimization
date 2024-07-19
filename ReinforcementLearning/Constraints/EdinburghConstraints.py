import numpy as np
from Environment.Grid import Grid
class EdinburghConstraints:

    def __init__(self, grid_width, grid_height, cost, tree_types_dict, generator):
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.cost_limit = cost
        self.tree_types_dict = tree_types_dict
        self.generator = generator
        self.planting_areas = Grid(grid_width, grid_height, 3)

    def evaluate(self, individual):
        total_cost = 0
        total_co2 = 0
        individual = individual.grid.numerical_grid.flatten()
        grid = [individual[i:i+ self.GRID_WIDTH] for i in range(0, len(individual), self.GRID_WIDTH)]

        total_quantity_credit_evergreen = 0
        total_quantity_credit_deciduous = 0
        total_trees = 0
        total_evergreen_trees = 0
        total_deciduous_trees = 0
        total_large_trees = 0 #large trees are trees with radius >= 20
        total_crown_area = 0

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell > 0:
                    tree = self.generator.generateTree(self.tree_types_dict[cell], (x, y))
                    total_cost += tree.getPrice()
                    total_co2 += tree.getCo2Absorption()
                    leaf_type = tree.getLeafType()
                    if leaf_type == "Evergreen":
                        total_quantity_credit_evergreen += tree.getCreditValue()
                        total_evergreen_trees += 1
                    elif leaf_type == "Deciduous":
                        total_quantity_credit_deciduous += tree.getCreditValue()
                        total_deciduous_trees += 1
                    if tree.getTreeCategory() == "Large":
                        total_large_trees += 1

                    total_trees += 1
                    total_crown_area += tree.getCrownArea()

        #############################
        min_trees_to_landscape = 0.2 * (7326) #7326 meters squared is plantable area of apartment complex
        min_evergreen_to_all = 0.2 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_large_to_all = 0.06 * total_trees
        max_canopy_coverage = 0.6 * (7326) #-1 because some regions not plantable
        min_canopy_coverage = 0.4 * (7326) #-1 because some regions not plantable
        min_evergreen_count = 0.015 * (total_evergreen_trees + total_deciduous_trees)
        min_deciduous_count = 0.015 * (total_evergreen_trees + total_deciduous_trees)
        #############################

        #################TREE RATIO CONSTRAINTS################
        if total_quantity_credit_evergreen + total_quantity_credit_deciduous < min_trees_to_landscape:
            print("total_quantity_credit_evergreen")
            return -100,
        elif total_quantity_credit_evergreen < min_evergreen_to_all:
            print("total_quantity_credit_evergreen")
            return -100,
        elif total_large_trees < min_large_to_all:
            print("total_large_trees")
            return -100,

        ################CANOPY COVERAGE CONSTRAINTS############
        if total_crown_area > max_canopy_coverage:
            print("total_crown_area above")
            return -100,
        elif total_crown_area < min_canopy_coverage:
            print("total_crown_area below")
            return -100,

        ################TREE COUNT CONSTRAINTS################
        if total_evergreen_trees < min_evergreen_count:
            print("total_evergreen_trees")
            return -100,
        elif total_deciduous_trees < min_deciduous_count:
            print("total_deciduous_trees")
            return -100,

        ################COST CONSTRAINTS################
        if total_cost > self.cost_limit:
            print("total_cost")
            return -100,
        return total_co2,

    def validate(self, individual):
        total_cost = 0
        total_co2 = 0
        grid = [individual[i:i+ self.GRID_WIDTH] for i in range(0, len(individual), self.GRID_WIDTH)]

        total_quantity_credit_evergreen = 0
        total_quantity_credit_deciduous = 0
        total_trees = 0
        total_evergreen_trees = 0
        total_deciduous_trees = 0
        total_large_trees = 0 #large trees are trees with radius >= 20
        total_crown_area = 0

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell > 0: #only check base of tree
                    tree = self.generator.generateTree(self.tree_types_dict[cell], (x, y))
                    total_cost += tree.getPrice()
                    total_co2 += tree.getCo2Absorption()
                    leaf_type = tree.getLeafType()
                    if leaf_type == "Evergreen":
                        total_quantity_credit_evergreen += tree.getCreditValue()
                        total_evergreen_trees += 1
                    elif leaf_type == "Deciduous":
                        total_quantity_credit_deciduous += tree.getCreditValue()
                        total_deciduous_trees += 1
                    if tree.getTreeCategory() == "Large":
                        total_large_trees += 1

                    total_trees += 1
                    total_crown_area += tree.getCrownArea()

        #############################
        min_trees_to_landscape = 0.2 * (7326)
        min_evergreen_to_all = 0.2 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_large_to_all = 0.06 * total_trees
        max_canopy_coverage = 0.6 * (7326) #-1 because some regions not plantable
        min_canopy_coverage = 0.4 * (7326) #-1 because some regions not plantable
        min_evergreen_count = 0.015 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_deciduous_count = 0.015 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        #############################

        #############TREE RATIO CONSTRAINTS################

        if total_quantity_credit_evergreen < min_evergreen_to_all:
            #print("Not enough evergreen trees to all trees " + str(total_quantity_credit_evergreen) + " < " +  str(min_evergreen_to_all))
            return "min_evergreen_to_all"
        elif total_large_trees < min_large_to_all:
            #print("Not enough large trees to all trees " + str(total_large_trees) + " < " + str(min_large_to_all))
            return "min_large_to_all"
        elif total_quantity_credit_evergreen + total_quantity_credit_deciduous < min_trees_to_landscape:
            #print("Not enough trees to landscape " + str(total_quantity_credit_evergreen) + " + " + str(total_quantity_credit_deciduous) + " < " + str(min_trees_to_landscape))
            return "min_trees_to_landscape"
        ############CANOPY COVERAGE CONSTRAINTS############
        if total_crown_area > max_canopy_coverage:
            #print("Canopy coverage exceeds " + str(total_crown_area))
            return "max_canopy_coverage"
        elif total_crown_area < min_canopy_coverage:
            #print("Canopy coverage below " + str(total_crown_area))
            return "min_canopy_coverage"
        ############TREE COUNT CONSTRAINTS################
        if total_evergreen_trees < min_evergreen_count:
            #print("Not enough evergreen trees " + str(total_evergreen_trees) + " < " + str(min_evergreen_count))
            return "min_evergreen_count"
        elif total_deciduous_trees < min_deciduous_count:
            #print("Not enough deciduous trees " + str(total_deciduous_trees) + " < " + str(min_deciduous_count))
            return "min_deciduous_count"
        ############COST CONSTRAINTS################
        if total_cost > self.cost_limit:
            #print("Cost exceeds " + str(total_cost))
            return "total_cost"



        #############VALID################
        print("VALID --- STATISTICS")
        print("Total CO2 Intake: " + str(total_co2))
        print("Trees to landscape - " + str(total_quantity_credit_evergreen) + " + " + str(total_quantity_credit_deciduous) + " > " + str(min_trees_to_landscape))
        print("Evergreen to all - " + str(total_quantity_credit_evergreen) + " > " +  str(min_evergreen_to_all))
        print("Large to all - " + str(total_large_trees) + " > " + str(min_large_to_all))
        print("Canopy coverage - " + str(total_crown_area) + " < " + str(max_canopy_coverage) + " and > " + str(min_canopy_coverage))
        print("Cost - " + str(total_cost) + " < " + str(self.cost_limit))