from deap import creator

class CustomIndividual(creator.Individual):
    def __init__(self):
        super().__init__()
        self.grid = None

    def __str__(self):
        return f'Individual(grid={self.grid})'