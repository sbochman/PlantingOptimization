import random

from Constraints.EdinburghConstraints import EdinburghConstraints
from Constraints.ScenarioOneConstraints import ScenarioOneConstraints
from Environment.Grid import Grid
import numpy as np
from deap import base, creator, tools, algorithms
import json
import matplotlib.pyplot as plt
from GeneticAlgorithm.GreedyInitGrid import GreedyInitGrid
from Trees.TreeSpacing import TreeSpacing
from Constraints.ScenarioTwoConstraints import ScenarioTwoConstraints
from GeneticAlgorithm.AlgorithmMutations import AlgorithmMutations
random.seed(100)

class CustomGeneticChanges:

    def __init__(self, x, y, trees_types_dict, generator, scenario):
        self.x = x
        self.y = y
        self.trees_types_dict = trees_types_dict
        self.generator = generator
        self.spacing = TreeSpacing(self.trees_types_dict)
        self.scenario = scenario
        self.COST_LIMIT = 530000 #cost limit set in paper
        self.co2_threshold = 3500
        self.NUM_TREES = 16 #number of tree types for park scenario

        self.iterations = 0 #limit number of attempts to find valid starting grid to prevent reaching max recursion depth
        self.previous_individual = None


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

    def mutate(self, individual, indpb):
        mutated = AlgorithmMutations(self.trees_types_dict, individual.grid)
        for i in range(individual.grid.y):
            for j in range(individual.grid.x):
                if random.random() < indpb:
                    #tree_type = random.choice([1,5,6,7,8,9,11,12,13,14,15,16,17,18,20,21])  #this line is for scenario 3 (edinburgh park)
                    tree_type = random.choice([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21]) #this line is for scenario 1 and 2
                    mutated.overlay_tree(tree_type, j, i)
        return individual


    def create_individual(self):
        individual = creator.Individual()
        individual.grid = Grid(self.x, self.y, self.scenario)
        return individual


    def run_edinburgh_scenario(self):
        cost = 50000
        fitness_eval = EdinburghConstraints(self.x, self.y, cost, self.trees_types_dict, self.generator)

        toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax, grid=None)

        #toolbox.register("attr_tree", lambda: next(generation_one))
        toolbox.register("individual", tools.initIterate, creator.Individual,
                         lambda: self.init_individual_edinburgh(fitness_eval))
        toolbox.register("population", tools.initRepeat, list, lambda: self.init_individual_edinburgh(fitness_eval))

        toolbox.register("evaluate", fitness_eval.evaluate)
        toolbox.register("mate", self.mate)
        toolbox.register("mutate", self.mutate, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Generate the initial population and run the genetic algorithm:
        population_size = 500
        population = toolbox.population(n=population_size)
        avg_scores = []
        best_scores = []
        NGEN = 100
        for gen in range(NGEN):
            print("Generation: ", gen)
            offspring = self.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            curr_avg = 0
            best_so_far = 0
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
                curr_avg += ind.fitness.values[0]
                best_so_far = max(best_so_far, ind.fitness.values[0])
            print("Best so far: ", best_so_far)

            #append top score to best_scores
            avg_scores.append(curr_avg / population_size)
            best_scores.append(best_so_far)
            population = toolbox.select(offspring, k=len(population))

        # Find and print the best solution found:
        best_ind = tools.selBest(population, 1)[0]
        print("Best individual is %s, %s" % (best_ind.grid, best_ind.fitness.values))
        fitness_eval.validate(best_ind.grid.numerical_grid.flatten())

        #save the best_grid list as a json file
        with open("best_grid_edinburgh_500.json", "w") as f:
            json.dump(best_ind.grid.numerical_grid.tolist(), f)

        #plot avg_scores
        self.plot_avg_scores(avg_scores)
        #save avg scores as img
        self.plot_best_scores(best_scores)



    def run_scenario_two(self):
        fitness_eval = ScenarioTwoConstraints(self.x, self.y, self.COST_LIMIT, self.trees_types_dict, self.generator)

        toolbox = base.Toolbox()
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMax, grid=None)

        toolbox.register("individual", tools.initIterate, creator.Individual, self.init_individual_scenario_two(fitness_eval))
        toolbox.register("population", tools.initRepeat, list, lambda: self.init_individual_scenario_two(fitness_eval))
        toolbox.register("evaluate", fitness_eval.evaluate)
        toolbox.register("mate", self.mate)
        toolbox.register("mutate", self.mutate, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Generate the initial population and run the genetic algorithm:
        population_size = 250
        population = toolbox.population(n=population_size)
        avg_scores = []
        best_scores = []
        NGEN = 100
        for gen in range(NGEN):
            print("Generation: ", gen)
            offspring = self.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            curr_avg = 0
            best_so_far = 0
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
                curr_avg += ind.fitness.values[0]
                best_so_far = max(best_so_far, ind.fitness.values[0])
            print("Best so far: ", best_so_far)

            #append top score to best_scores
            avg_scores.append(curr_avg / population_size)
            best_scores.append(best_so_far)
            population = toolbox.select(offspring, k=len(population))

        # Find and print the best solution found:
        best_ind = tools.selBest(population, 1)[0]
        print("Best individual is %s, %s" % (best_ind.grid, best_ind.fitness.values))
        fitness_eval.validate(best_ind.grid.numerical_grid.flatten())

        #save the best_grid list as a json file
        with open("best_grid_s2_500.json", "w") as f:
            json.dump(best_ind.grid.numerical_grid.tolist(), f)

        #plot avg_scores
        self.plot_avg_scores(avg_scores)
        #save avg scores as img
        self.plot_best_scores(best_scores)

    def plot_avg_scores(self, scores):
        plt.plot(scores)
        plt.xlabel('Generation')
        plt.ylabel('Average Fitness')
        plt.title('Average Fitness vs Generation')
        #save as img
        plt.savefig('average_fitness_s1_500_50gen.png')
        plt.show()

    def plot_best_scores(self, scores):
        plt.plot(scores)
        plt.xlabel('Generation')
        plt.ylabel('Best Fitness')
        plt.title('Best Fitness vs Generation')
        #save as img
        plt.savefig('best_fitness_s1_500_50gen.png')
        plt.show()

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


    def run_scenario_one(self):
        fitness_eval = ScenarioOneConstraints(self.x, self.y, self.co2_threshold, self.trees_types_dict, self.generator)

        toolbox = base.Toolbox()
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin, grid=None)
        toolbox.register("individual", tools.initIterate, creator.Individual, self.init_individual_scenario_one(fitness_eval))
        toolbox.register("population", tools.initRepeat, list, lambda: self.init_individual_scenario_one(fitness_eval))
        toolbox.register("evaluate", fitness_eval.evaluate)
        toolbox.register("mate", self.mate)
        toolbox.register("mutate", self.mutate, indpb=0.05)
        toolbox.register("select", tools.selTournament, tournsize=3)

        # Generate the initial population and run the genetic algorithm:
        population_size = 500
        population = toolbox.population(n=population_size)
        avg_scores = []
        best_scores = []
        NGEN = 50
        for gen in range(NGEN):
            print("Generation: ", gen)
            offspring = self.varAnd(population, toolbox, cxpb=0.5, mutpb=0.2)
            fits = toolbox.map(toolbox.evaluate, offspring)
            curr_avg = 0
            best_so_far = float('inf')
            for fit, ind in zip(fits, offspring):
                ind.fitness.values = fit
                curr_avg += ind.fitness.values[0]
                best_so_far = min(best_so_far, ind.fitness.values[0])
            print("Best so far: ", best_so_far)

            #append top score to best_scores
            avg_scores.append(curr_avg / population_size)
            best_scores.append(best_so_far)
            population = toolbox.select(offspring, k=len(population))

        # Find and print the best solution found:
        best_ind = tools.selBest(population, 1)[0]
        print("Best individual is %s, %s" % (best_ind.grid, best_ind.fitness.values))
        fitness_eval.validate(best_ind.grid.numerical_grid.flatten())

        #save the best_grid list as a json file
        with open("best_grid_scenario_one_500_50gen.json", "w") as f:
            json.dump(best_ind.grid.numerical_grid.tolist(), f)

        #plot avg_scores
        self.plot_avg_scores(avg_scores)
        #save avg scores as img
        self.plot_best_scores(best_scores)


    def get_tree_generator(self, start_grid):
        def predefined_tree():
            return [tree for tree in start_grid]
        return predefined_tree

    def init_individual_scenario_two(self, fitness_eval):
        #init start grid and validate that the grid abides constraints
        self.iterations+=1
        print("Iteration: " + str(self.iterations))
        init_individual = self.create_individual()
        mutations = AlgorithmMutations(self.trees_types_dict, init_individual.grid)
        greedy_alg = GreedyInitGrid(self.x, self.y, init_individual, self.trees_types_dict, self.generator, fitness_eval, mutations)
        start_ind = greedy_alg.init_grid_scenario_two()
        if self.iterations > 650:
            self.iterations = 0
            print("No valid configuration found, returning previous individual")
            return self.previous_individual #to prevent max recursion depth set current population to the last one
        if start_ind == None: return self.init_individual_scenario_two(fitness_eval)
        #set previous individual to current individual
        self.previous_individual = start_ind
        return start_ind

    def init_individual_scenario_one(self, fitness_eval):
        self.iterations+=1
        print("Iteration: " + str(self.iterations))
        init_individual = self.create_individual()
        mutations = AlgorithmMutations(self.trees_types_dict, init_individual.grid)
        greedy_alg = GreedyInitGrid(self.x, self.y, init_individual, self.trees_types_dict, self.generator, fitness_eval, mutations)
        start_ind = greedy_alg.init_grid_scenario_one()
        if self.iterations > 650:
            self.iterations = 0
            print("No valid configuration found, returning previous individual")
            return self.previous_individual #to prevent max recursion depth set current population to the last one
        if start_ind == None: return self.init_individual_scenario_one(fitness_eval)
        #set previous individual to current individual
        self.previous_individual = start_ind
        return start_ind

    def init_individual_edinburgh(self, fitness_eval):
        self.iterations+=1
        print("Iteration: " + str(self.iterations))
        init_individual = self.create_individual()
        mutations = AlgorithmMutations(self.trees_types_dict, init_individual.grid)
        greedy_alg = GreedyInitGrid(self.x, self.y, init_individual, self.trees_types_dict, self.generator, fitness_eval, mutations)
        start_ind = greedy_alg.init_grid_edinburgh()
        if self.iterations > 650:
            self.iterations = 0
            print("No valid configuration found, returning previous individual")
            return self.previous_individual #to prevent max recursion depth set current population to the last one
        if start_ind == None: return self.init_individual_edinburgh(fitness_eval)
        #set previous individual to current individual
        self.previous_individual = start_ind
        return start_ind