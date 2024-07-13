import random
from Environment.Grid import Grid
import numpy as np
from deap import base, creator, tools, algorithms
import matplotlib.pyplot as plt
from GeneticAlgorithm.GreedyInitGrid import GreedyInitGrid
from Trees.TreeSpacing import TreeSpacing
from ScenarioTwoConstraints.Constraints import Constraints
from GeneticAlgorithm.AlgorithmMutations import AlgorithmMutations
random.seed(100)

class CustomGeneticChanges:

    def __init__(self, x, y, trees_types_dict, generator):
        self.x = x
        self.y = y
        self.trees_types_dict = trees_types_dict
        self.generator = generator
        self.spacing = TreeSpacing(self.trees_types_dict)

        self.COST_LIMIT = 40000
        self.NUM_TREES = 21

        #fitness eval init
        self.fitness_eval = Constraints(self.x, self.y, self.COST_LIMIT, self.trees_types_dict, self.generator)


    def mate(self, ind1, ind2):
        ind1_grid_flat = ind1.grid.numerical_grid.flatten()
        ind2_grid_flat = ind2.grid.numerical_grid.flatten()

        size = min(len(ind1_grid_flat), len(ind2_grid_flat))
        cxpoint = random.randint(1, size - 1)

        # Perform one-point crossover
        offspring1 = list(ind1_grid_flat[:cxpoint]) + list(ind2_grid_flat[cxpoint:])
        offspring2 = list(ind2_grid_flat[:cxpoint]) + list(ind1_grid_flat[cxpoint:])


        #make crossovers 2d arrays
        offspring1 = np.array(offspring1).reshape(self.y, self.x)
        offspring2 = np.array(offspring2).reshape(self.y, self.x)

        #make new individuals
        ind1 = self.create_individual()
        ind2 = self.create_individual()
        #make AlgorithmMutations objects for each individual
        mutated_ind1 = AlgorithmMutations(self.trees_types_dict, ind1.grid)
        mutated_ind2 = AlgorithmMutations(self.trees_types_dict, ind2.grid)

        #fill in temporary grids with offspring crossovers to determine valid planting (spatial constraint)
        for i in range(self.y):
            for j in range(self.x):
                #if offspring1[i][j] or offspring2[i][j] is a val > 0, then it is base of tree and position to plant
                if offspring1[i][j] > 0:
                    #call plant function, if its not plantable in that position, will not plant
                    mutated_ind1.plant_tree(offspring1[i][j], j, i) #if not plantable will not plant
                if offspring2[i][j] > 0:
                    mutated_ind2.plant_tree(offspring2[i][j], j, i) #if not plantable will not plant


        #return offspring1, offspring2 as flattened arrays
        return ind1, ind2

    def mutate(self, individual, low, up, indpb):
        mutated = AlgorithmMutations(self.trees_types_dict, individual.grid)
        for i in range(individual.grid.y):
            for j in range(individual.grid.x):
                if random.random() < indpb:
                    tree_type = random.randint(low, up)
                    mutated.overlay_tree(tree_type, j, i)
        return individual


    def create_individual(self):
        individual = creator.Individual()
        individual.grid = Grid(self.x, self.y)
        return individual

    def run(self):
        COST_LIMIT = 800000
        fitness_eval = Constraints(self.x, self.y, COST_LIMIT, self.trees_types_dict, self.generator)

        #creator.create("FitnessMax", base.Fitness, weights=(1.0,))  # Maximize the fitness
        #creator.create("Individual", list, fitness=creator.FitnessMax, grid=None)


        toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax, grid=None)

        #toolbox.register("attr_tree", lambda: next(generation_one))
        toolbox.register("individual", tools.initIterate, creator.Individual,
                         self.init_individual)   #self.get_tree_generator(start_ind.grid.numerical_grid))   #, n=GRID_WIDTH*GRID_HEIGHT)
        toolbox.register("population", tools.initRepeat, list, self.init_individual)

        toolbox.register("evaluate", fitness_eval.evaluate)
        toolbox.register("mate", self.mate)
        toolbox.register("mutate", self.mutate, low=0, up=self.NUM_TREES, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Generate the initial population and run the genetic algorithm:
        population = toolbox.population(n=250)
        #population[0].grid.print_grid()
        NGEN = 5
        for gen in range(NGEN):
            offspring = self.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
                print(ind.fitness.values)
            population = toolbox.select(offspring, k=len(population))

        # Find and print the best solution found:
        best_ind = tools.selBest(population, 1)[0]
        print("Best individual is %s, %s" % (best_ind.grid, best_ind.fitness.values))
        fitness_eval.validate(best_ind.grid.numerical_grid.flatten())

        def individual_to_grid(individual, width, height):
            return [individual[i:i + width] for i in range(0, len(individual), width)]

        # Convert the best individual into a grid
        best_grid = individual_to_grid(best_ind.grid.numerical_grid, self.x, self.y)

        # Print the grid
        best_ind.grid.print_grid()

        print(fitness_eval.validate(best_ind))

        self.plot_grid(best_ind.grid.numerical_grid)

    def plot_grid(self, grid):
        array = np.array(grid)
        plt.figure(figsize=(30, 30))
        plt.imshow(array, cmap='viridis', interpolation='nearest')
        plt.colorbar(label='Tree Types')
        plt.title('Planting Grid Visualization')
        plt.show()

    def varAnd(self, population, toolbox, cxpb, mutpb):
        offspring = [toolbox.clone(ind) for ind in population]

        # Apply crossover and mutation on the offspring
        for i in range(1, len(offspring), 2):
            if random.random() < cxpb:
                offspring[i - 1], offspring[i] = toolbox.mate(offspring[i - 1], offspring[i])
                del offspring[i - 1].fitness.values, offspring[i].fitness.values

        for i in range(len(offspring)):
            if random.random() < mutpb:
                offspring[i] = toolbox.mutate(offspring[i])
                del offspring[i].fitness.values

        return offspring

    def get_tree_generator(self, start_grid):
        def predefined_tree():
            return [tree for tree in start_grid]
        return predefined_tree

    def init_individual(self):
        #init start grid and validate that the grid abides constraints
        init_individual = self.create_individual()
        mutations = AlgorithmMutations(self.trees_types_dict, init_individual.grid)
        greedy_alg = GreedyInitGrid(self.x, self.y, init_individual, self.trees_types_dict, self.generator, self.fitness_eval, mutations)
        start_ind = greedy_alg.init_grid()
        if start_ind == None: return self.init_individual()
        return start_ind