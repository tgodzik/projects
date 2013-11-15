__author__ = 'Tomasz Godzik'

from utils.reader import *
from utils.evolution import *
from deap import base
from deap import creator
from deap import tools

#read the problem from file
problem=from_file(["./solomon_25/C101.txt"])[0]

#count the number of customers
customers_num=len(problem.customers.keys())

# create fitness and individual
creator.create("FitnessSolution", base.Fitness, weights=(-1.0, -0.1))
creator.create("Individual", list, fitness=creator.FitnessSolution)

#create list of all customers
customer=range(1,customers_num+1)


#creating new individuals
toolbox = base.Toolbox()
toolbox.register("attr", randomize_list,customer,problem.vehicles)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

toolbox.register("evaluate", evaluate, problem)
#cross - ind1, ind2
#toolbox.register("mate", tools.cxTwoPoints)
# mutate with one ind
toolbox.register("mutate", mutate, problem.vehicles)
# ind, k <- NGSA, SPEA
#toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

NGEN=40

ind1 = toolbox.individual()

ind1.fitness.values = evaluate(ind1,problem)
print ind1.fitness.valid
print ind1.fitness
print ind1
ind2, = mutate(ind1,problem.vehicles)
ind2.fitness.values = evaluate(ind2,problem)
print ind2.fitness.valid
print ind2.fitness
print ind2

#
#ind2.fitness.values = evaluate(ind2,problem)
#print ind2.fitness.valid
#print ind2.fitness

#for g in range(NGEN):
#    # Select the next generation individuals
#    offspring = toolbox.select(pop, len(pop))
#    # Clone the selected individuals
#    offspring = map(toolbox.clone, offspring)
#
#    # Apply crossover on the offspring
#    for child1, child2 in zip(offspring[::2], offspring[1::2]):
#        if random.random() < CXPB:
#            toolbox.mate(child1, child2)
#            del child1.fitness.values
#            del child2.fitness.values
#
#    # Apply mutation on the offspring
#    for mutant in offspring:
#        if random.random() < MUTPB:
#            toolbox.mutate(mutant)
#            del mutant.fitness.values
#
#    # Evaluate the individuals with an invalid fitness
#    invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
#    fitnesses = toolbox.map(toolbox.evaluate, invalid_ind)
#    for ind, fit in zip(invalid_ind, fitnesses):
#        ind.fitness.values = fit
#
#    # The population is entirely replaced by the offspring
#    pop[:] = offspring