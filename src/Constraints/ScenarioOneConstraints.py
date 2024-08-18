from Environment.Grid import Grid
class ScenarioOneConstraints:
    """
    ScenarioOneConstraints class is used to evaluate the fitness of an individual in the first scenario. The first scenario here minimises cost
    of the apartment complex while ensuring that the CO2 absorption of the trees planted is greater than a certain threshold.

    Attributes:
        grid_width (int): The width of the grid
        grid_height (int): The height of the grid
        co2_threshold (int): The threshold of CO2 absorption that the trees planted must exceed
        tree_types_dict (dict): A dictionary containing the tree types and their respective values
        generator (TreeGenerator): A TreeGenerator object that is used to generate trees
    """
    def __init__(self, grid_width, grid_height, co2_threshold, tree_types_dict, generator):
        """
        Constructor for the ScenarioOneConstraints class
        :param grid_width: grid width
        :param grid_height: grid height
        :param co2_threshold: co2 threshold, which is set to 3500 kg/year in the paper
        :param tree_types_dict: dictionary containing tree types id and their respective species
        :param generator: TreeGenerator object to generate trees
        """
        self.GRID_WIDTH = grid_width
        self.GRID_HEIGHT = grid_height
        self.co2_threshold = co2_threshold
        self.tree_types_dict = tree_types_dict
        self.generator = generator
        self.planting_areas = Grid(grid_width, grid_height, 1)

    def evaluate(self, individual):
        """
        Evaluate the fitness of an individual. The fitness is calculated based on the cost of the trees planted.
        If the individual does not meet the constraints, the fitness is set to 999999.

        :param individual: chromosome to evaluate
        :return: integer fitness value
        """

        #keep track of cost and co2
        total_cost = 0
        total_co2 = 0
        #flatten the grid
        individual = individual.grid.numerical_grid.flatten()
        grid = [individual[i:i+ self.GRID_WIDTH] for i in range(0, len(individual), self.GRID_WIDTH)]

        #keep track of tree statistics
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
        num_native_road = 0
        total_native_road_interval = 0
        total_pedestrian_road_interval = 0

        #iterate through the grid and increment the statistics
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
                        if tree.getTreeCategory() == "Native":
                            num_native_road += 1
                            total_native_road_interval += tree.plant_size[1]
                    elif self.planting_areas.grid[y][x].pedestrian_road: #check if square is pedestrian road
                        num_trees_pedestrian += 1
                        total_pedestrian_road_interval += tree.plant_size[1]

                    total_trees += 1
                    total_crown_area += tree.getCrownArea()


        #constraints as indicated in the paper
        #############################
        min_trees_to_landscape = 0.2 * (7326) #7326 meters squared is plantable area of apartment complex
        min_evergreen_to_all = 0.2 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_native_to_all = 0.1 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_large_to_all = 0.06 * total_trees
        max_canopy_coverage = 0.6 * (7326) #-1 because some regions not plantable
        min_canopy_coverage = 0.4 * (7326) #-1 because some regions not plantable
        min_evergreen_count = 0.015 * (total_evergreen_trees + total_deciduous_trees)
        min_deciduous_count = 0.015 * (total_evergreen_trees + total_deciduous_trees)
        #############################

        #################TREE RATIO CONSTRAINTS################
        if total_quantity_credit_evergreen + total_quantity_credit_deciduous < min_trees_to_landscape:
            print("total_quantity_credit_evergreen")
            return 999999,
        elif total_quantity_credit_evergreen < min_evergreen_to_all:
            print("total_quantity_credit_evergreen")
            return 999999,
        elif total_quantity_credit_native < min_native_to_all:
            print("total_quantity_credit_native")
            return 999999,
        elif total_large_trees < min_large_to_all:
            print("total_large_trees")
            return 999999,

        ################CANOPY COVERAGE CONSTRAINTS############
        if total_crown_area > max_canopy_coverage:
            print("total_crown_area above")
            return 999999,
        elif total_crown_area < min_canopy_coverage:
            print("total_crown_area below")
            return 999999,

        ################TREE COUNT CONSTRAINTS################
        if total_evergreen_trees < min_evergreen_count:
            print("total_evergreen_trees")
            return 999999,
        elif total_deciduous_trees < min_deciduous_count:
            print("total_deciduous_trees")
            return 999999,
        ############ROAD SIDE PLANTING################
        if num_native_road * (total_native_road_interval / num_native_road) < 148: #meter length of road. keep 10 meter interval between. seems as though paper used 10 meters given 20 native trees planted
            print("Not enough trees planted by road " + str(num_native_road * 2) + " < " + str(148))
            return 999999,
        ############PEDESTRIAN ROAD PLANTING################
        if num_trees_pedestrian * (total_pedestrian_road_interval / num_trees_pedestrian) < 186: #meter length of pedestrian road. multiple by 4 since the interva is set to 8 blocks (4 meters)
            print("Not enough trees planted by pedestrian road " + str(num_trees_pedestrian * 2) + " < " + str(186))
            return 999999,
        #############Hedge Planting################
        if total_crown_hedge < 360: #meter length of hedge zone
            print("total_crown_hedge")
            return 999999,

        ################CO2 CONSTRAINT################
        if total_co2 < self.co2_threshold:
            print("total_cost")
            return 999999,
        return total_cost,

    def validate(self, individual):
        """
        Validate the individual based on the constraints. If the individual does not meet the constraints, print the constraint that is violated.
        Otherwise, print "VALID". This is used in the greedy algorithm to determine what constraint is currently being violated.

        :param individual: chromosome to validate
        :return: string indicating the constraint that is violated or "VALID" if valid
        """

        #keep track of cost and co2
        total_cost = 0
        total_co2 = 0
        #flatten the grid
        grid = [individual[i:i+ self.GRID_WIDTH] for i in range(0, len(individual), self.GRID_WIDTH)]

        #track tree statistics
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
        num_native_road = 0
        total_native_road_interval = 0
        total_pedestrian_road_interval = 0

        #iterate through the grid and increment the statistics
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
                        if tree.getTreeCategory() == "Native":
                            num_native_road += 1
                            total_native_road_interval += tree.plant_size[1]
                    elif self.planting_areas.grid[y][x].pedestrian_road: #check if square is pedestrian road
                        num_trees_pedestrian += 1
                        total_pedestrian_road_interval += tree.plant_size[1]

                    total_trees += 1
                    total_crown_area += tree.getCrownArea()

        #constraints as indicated in the paper
        #############################
        min_trees_to_landscape = 0.2 * (7326)
        min_evergreen_to_all = 0.2 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
        min_native_to_all = 0.1 * (total_quantity_credit_evergreen + total_quantity_credit_deciduous)
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
        if num_native_road * (total_native_road_interval / num_native_road) < 148: #meter length of road. keep 10 meter interval between. seems as though paper used 10 meters given 20 native trees planted
            #print("Not enough trees planted by road " + str(num_native_road * 2) + " < " + str(148))
            return "road_side_planting"
        ############PEDESTRIAN ROAD PLANTING################
        if num_trees_pedestrian * (total_pedestrian_road_interval / num_trees_pedestrian) < 186: #meter length of pedestrian road. multiple by 4 since the interva is set to 8 blocks (4 meters)
            #print("Not enough trees planted by pedestrian road " + str(num_trees_pedestrian * 2) + " < " + str(186))
            return "pedestrian_road_planting"
        #############Hedge Planting################
        if total_crown_hedge < 360: #meter length of hedge zone
            #print("Not enough trees planted by hedge " + str(total_crown_hedge) + " < " + str(0.1 * total_crown_area))
            return "hedge_planting"
        ############CO2 CONSTRAINT################
        if total_co2 < self.co2_threshold:
            #print("Cost exceeds " + str(total_cost))
            return "total_cost"

        #############VALID################
        print("VALID --- STATISTICS")
        print("Total CO2 Intake: " + str(total_co2) + " < " + str(self.co2_threshold))
        print("Trees to landscape - " + str(total_quantity_credit_evergreen) + " + " + str(total_quantity_credit_deciduous) + " > " + str(min_trees_to_landscape))
        print("Evergreen to all - " + str(total_quantity_credit_evergreen) + " > " +  str(min_evergreen_to_all))
        print("Native to all - " + str(total_quantity_credit_native) + " > "  + str(min_native_to_all))
        print("Large to all - " + str(total_large_trees) + " > " + str(min_large_to_all))
        print("Canopy coverage - " + str(total_crown_area) + " < " + str(max_canopy_coverage) + " and > " + str(min_canopy_coverage))
        print("Cost - " + str(total_cost))
