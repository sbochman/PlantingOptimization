import numpy as np
from Environment.Grid import Grid
class Constraints:

    def __init__(self, grid_width, grid_height, cost_limit, tree_types_dict, generator):
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.cost_limit = cost_limit
        self.tree_types_dict = tree_types_dict
        self.generator = generator
        self.planting_areas = Grid(grid_width, grid_height)

    def evaluate(self, individual):
        total_cost = 0
        total_co2 = 0
        individual = individual.grid.numerical_grid.flatten()
        grid = [individual[i:i+ self.GRID_WIDTH] for i in range(0, len(individual), self.GRID_WIDTH)]

        total_quantity_credit_evergreen = 0
        total_quantity_credit_deciduous = 0
        total_quantity_credit_native = 0
        total_trees = 0
        total_evergreen_trees = 0
        total_deciduous_trees = 0
        total_large_trees = 0 #large trees are trees with radius >= 20
        total_crown_area = 0
        total_crown_hedge = 0
        num_trees_road = 0
        num_trees_pedestrian = 0

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
                    elif tree.getTreeCategory() == "Native":
                        total_quantity_credit_native += tree.getCreditValue()

                    if self.planting_areas.grid[y][x].hedge: #check if square is hedge
                        total_crown_hedge += tree.getCrownArea()
                    elif self.planting_areas.grid[y][x].road: #check if square is road
                        num_trees_road += 1
                    elif self.planting_areas.grid[y][x].pedestrian_road: #check if square is pedestrian road
                        num_trees_pedestrian += 1

                    total_trees += 1
                    total_crown_area += tree.getCrownArea()

        #############################
        min_trees_to_landscape = 0.2 * (self.GRID_WIDTH * self.GRID_HEIGHT - 50)
        min_evergreen_to_all = 0.2 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_native_to_all = 0.1 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_large_to_all = 0.06 * total_trees
        max_canopy_coverage = 0.6 * (self.GRID_WIDTH * self.GRID_HEIGHT - 50) #-1 because some regions not plantable
        min_canopy_coverage = 0.4 * (self.GRID_WIDTH * self.GRID_HEIGHT - 50) #-1 because some regions not plantable
        min_evergreen_count = 0.015 * (total_evergreen_trees + total_deciduous_trees)
        min_deciduous_count = 0.015 * (total_evergreen_trees + total_deciduous_trees)
        road_side_planting = 4 * num_trees_road #interval of 4 meters
        pedestrian_road_planting = 4 * num_trees_pedestrian #interval of 4 meters
        #############################

        #################TREE RATIO CONSTRAINTS################
        if total_quantity_credit_evergreen + total_quantity_credit_deciduous < min_trees_to_landscape:
            return -100,
        elif total_quantity_credit_evergreen < min_evergreen_to_all:
            return -100,
        elif total_quantity_credit_native < min_native_to_all:
            return -100,
        elif total_large_trees < min_large_to_all:
            return -100,

        ################CANOPY COVERAGE CONSTRAINTS############
        if total_crown_area > max_canopy_coverage:
            return -100,
        elif total_crown_area < min_canopy_coverage:
            return -100,

        ################TREE COUNT CONSTRAINTS################
        if total_evergreen_trees < min_evergreen_count:
            return -100,
        elif total_deciduous_trees < min_deciduous_count:
            return -100,

        ############ROAD SIDE PLANTING################
        if road_side_planting < 148: #meter length of road
            return -100,
        ############PEDESTRIAN ROAD PLANTING################
        if pedestrian_road_planting < 186: #meter length of pedestrian road
            return -100,
        #############Hedge Planting################
        if total_crown_hedge < 360: #meter length of hedge zone
            return -100,

        ################COST CONSTRAINTS################
        if total_cost > self.cost_limit:
            return -100,
        return total_co2,

    def validate(self, individual):
        total_cost = 0
        total_co2 = 0
        grid = [individual[i:i+ self.GRID_WIDTH] for i in range(0, len(individual), self.GRID_WIDTH)]

        total_quantity_credit_evergreen = 0
        total_quantity_credit_deciduous = 0
        total_quantity_credit_native = 0
        total_trees = 0
        total_evergreen_trees = 0
        total_deciduous_trees = 0
        total_large_trees = 0 #large trees are trees with radius >= 20
        total_crown_area = 0
        total_crown_hedge = 0
        num_trees_road = 0
        num_trees_pedestrian = 0

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
                    elif tree.getTreeCategory() == "Native":
                        total_quantity_credit_native += tree.getCreditValue()

                    if self.planting_areas.grid[y][x].hedge: #check if square is hedge
                        total_crown_hedge += tree.getCrownArea()
                    elif self.planting_areas.grid[y][x].road: #check if square is road
                        num_trees_road += 1
                    elif self.planting_areas.grid[y][x].pedestrian_road: #check if square is pedestrian road
                        num_trees_pedestrian += 1

                    total_trees += 1
                    total_crown_area += tree.getCrownArea()

        #############################
        min_trees_to_landscape = 0.2 * (self.GRID_WIDTH * self.GRID_HEIGHT - 50)  #-1 because some regions not plantable
        min_evergreen_to_all = 0.2 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_native_to_all = 0.1 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_large_to_all = 0.06 * total_trees
        max_canopy_coverage = 0.6 * (self.GRID_WIDTH * self.GRID_HEIGHT - 50) #-1 because some regions not plantable
        min_canopy_coverage = 0.4 * (self.GRID_WIDTH * self.GRID_HEIGHT - 50) #-1 because some regions not plantable
        min_evergreen_count = 0.015 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_deciduous_count = 0.015 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        road_side_planting = 4 * num_trees_road #interval of 4 meters
        pedestrian_road_planting = 4 * num_trees_pedestrian #interval of 4 meters
        #############################

        #############TREE RATIO CONSTRAINTS################

        if total_quantity_credit_evergreen < min_evergreen_to_all:
            #print("Not enough evergreen trees to all trees " + str(total_quantity_credit_evergreen) + " < " +  str(min_evergreen_to_all))
            return "min_evergreen_to_all"
        elif total_quantity_credit_native < min_native_to_all:
            #print("Not enough native trees to all trees " + str(total_quantity_credit_native) + " < "  + str(min_native_to_all))
            return "min_native_to_all"
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
        ############ROAD SIDE PLANTING################
        if road_side_planting < 148: #meter length of road
            #print("Not enough trees planted by road " + str(road_side_planting) + " < " + str(num_trees_road))
            return "road_side_planting"
        ############PEDESTRIAN ROAD PLANTING################
        if pedestrian_road_planting < 186: #meter length of pedestrian road
            #print("Not enough trees planted by pedestrian road " + str(pedestrian_road_planting) + " < " + str(num_trees_pedestrian))
            return "pedestrian_road_planting"
        #############Hedge Planting################
        if total_crown_hedge < 360: #meter length of hedge zone
            #print("Not enough trees planted by hedge " + str(total_crown_hedge) + " < " + str(0.1 * total_crown_area))
            return "hedge_planting"
        ############COST CONSTRAINTS################
        if total_cost > self.cost_limit:
            #print("Cost exceeds " + str(total_cost))
            return "total_cost"



        #############VALID################
        print("VALID --- STATISTICS")
        print("Total CO2 Intake: " + str(total_co2))
        print("Trees to landscape - " + str(total_quantity_credit_evergreen) + " + " + str(total_quantity_credit_deciduous) + " > " + str(min_trees_to_landscape))
        print("Evergreen to all - " + str(total_quantity_credit_evergreen) + " > " +  str(min_evergreen_to_all))
        print("Native to all - " + str(total_quantity_credit_native) + " > "  + str(min_native_to_all))
        print("Large to all - " + str(total_large_trees) + " > " + str(min_large_to_all))
        print("Canopy coverage - " + str(total_crown_area) + " < " + str(max_canopy_coverage) + " and > " + str(min_canopy_coverage))
        print("Cost - " + str(total_cost) + " < " + str(self.cost_limit))
