## Genetic Algorithm

This project focuses on optimizing tree planting strategies in two distinct locations: an apartment complex in Seoul, South Korea, and Sundial Garden at Inverleith Park, Edinburgh, Scotland. Using a genetic algorithm, the aim is to maximize CO2 absorption while minimizing the costs associated with planting trees in these complex environments.

Choi and Lee utilise a linear programming solution in their optimisation strategy, which can be read here: https://link.springer.com/article/10.1007/s11355-022-00524-8

This project recretes the apartment complex and compares the genetic algorithm to Choi and Lee's solution. The project as is beats the linear programming solution when maximising CO2 absorption, but fails to beat Choi and Lee when minimising cost.


## Running Project

To run this code, first ensure the proper dependencies and versions are installed. In the src files, Run.py runs the algorithm. You can run this by using python Run.py in the command prompt, bash, or terminal.

To run different scenarios, change line 66 in Run.py to custom_genetic.run_scenario_one(), custom_genetic.run_scenario_two(), or custom_genetic.run_edinburgh_scenario().

Additionally, in GeneticAlgorithm/CustomGeneticChanges.py, the population_size and NGEN variables can be changed to try different population sizes and run for varied amounts of iterations.

The result of the program is two output images (graphs) of the average fitness score for each generation, best fitness score for each generation, and the resulting best 2D grid as a JSON file.

## Dependencies

This project requires the following Python libraries:

- **pandas** (2.2.2)
- **matplotlib** (3.9.1) and **seaborn** (0.13.2)
- **scipy** (1.14.0)
- **numpy** (1.26.4)
- **DEAP** (1.4.1)

