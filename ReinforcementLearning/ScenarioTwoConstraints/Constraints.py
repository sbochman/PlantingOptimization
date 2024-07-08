class Constraints:

    def __init__(self, plantable_spots_remaining):
        self.reward = 0
        self.total_co2 = 0
        self.above_co2_threshold = False
        self.number_co2_over_threshold = 0
        self.total_cost = 0
        self.below_cost_threshold = True
        self.plantable_spots_remaining = plantable_spots_remaining
        self.total_spots = plantable_spots_remaining
        self.tree_types = []

    def calculate_reward(self, action, tree, grid, state):
        curr_reward = 0

        co2_absorption = tree.getCo2Absorption()
        cost = tree.getPrice()

        if self.below_cost_threshold:
            curr_reward += 3
        else:
            curr_reward -= 50

        curr_reward += 2 * co2_absorption

        return curr_reward

    def maximize_co2_constraint(self, action):
        tree = action
        self.total_co2 += tree.getCo2Absorption()
        if self.total_co2 > 30:
            self.above_co2_threshold = True
            self.number_co2_over_threshold += 1
        return tree.getCo2Absorption()

    def cost_limitation_constraint(self, action):
        tree = action
        self.total_cost += tree.getPrice()
        if self.total_cost < 10000:
            self.below_cost_threshold = True
        else:
            self.below_cost_threshold = False
        return tree.getPrice()
