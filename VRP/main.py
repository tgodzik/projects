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

toolbox.register("evaluate", evaluate)
#cross - ind1, ind2
#toolbox.register("mate", tools.cxTwoPoints)
# mutate with one ind
#toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
# ind, k <- NGSA, SPEA
#toolbox.register("select", tools.selTournament, tournsize=3)

population = toolbox.population(n=300)

NGEN=40

#ind1.fitness.values = evaluate(ind1,problem)
#print ind1.fitness.valid
#print ind1.fitness
#
#ind2.fitness.values = evaluate(ind2,problem)
#print ind2.fitness.valid
#print ind2.fitness