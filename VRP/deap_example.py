import random

from deap import base
from deap import creator
from deap import tools

IND_SIZE = 5

creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)

toolbox = base.Toolbox()
toolbox.register("attr_list", random.random)
toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_float, n=IND_SIZE)

ind1 = toolbox.individual()

print ind1               # [0.86..., 0.27..., 0.70..., 0.03..., 0.87...]
print ind1.fitness.valid # False

#wyliczamy wartosc fitness
def evaluate(individual):
    # Do some hard computing on the individual
    a = sum(individual)
    b = len(individual)
    return a, 1. / b

ind1.fitness.values = evaluate(ind1)
print ind1.fitness.valid    # True
print ind1.fitness          # (2.73, 0.2)

mutant = toolbox.clone(ind1)
ind2, = tools.mutGaussian(mutant, mu=0.0, sigma=0.2, indpb=0.2)
del mutant.fitness.values

print ind2               # [0.86..., 0.27..., 0.70..., 0.03..., 0.87...]
print ind2.fitness.valid # False

child1, child2 = [toolbox.clone(ind) for ind in (ind1, ind2)]
tools.cxBlend(child1, child2, 0.5)
del child1.fitness.values
del child2.fitness.values

print child1