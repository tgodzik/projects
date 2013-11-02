__author__ = 'Tomasz Godzik'

from utils.reader import *
from deap import base
from deap import creator
from deap import tools

problem=from_file(["./solomon_25/C101.txt"])[0]

customers_num=len(problem.customers.keys())

# number of vehicles, total distance
creator.create("FitnessSolution", base.Fitness, weights=(-1.0, -0.1))
creator.create("Individual", list, fitness=creator.FitnessSolution)

customer=range(1,customers_num+1)


toolbox = base.Toolbox()
toolbox.register("attr", randomize_list,customer,problem.vehicles)
toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.attr)

ind1 = toolbox.individual()
ind2 = toolbox.individual()

print ind1
print ind2

def evaluate_route(route,problem):
    time=0
    current_cargo=problem.capacity
    current_x=problem.depotx
    current_y=problem.depoty
    for i in route:
        #calculate the distance from one customer to another
        dist=math.sqrt(math.pow(problem.customers[i].x-current_x,2)+math.pow(problem.customers[i].y-current_y,2))
        current_x=problem.customers[i].x
        current_y=problem.customers[i].y
        time+=dist
        #if we have to wait
        time=max(time<problem.customers[i].ready, time)
    return time

#wyliczamy wartosc fitness
def evaluate(individual,problem):
    a =  len(individual)
    b=0
    for i in individual:
        b+=evaluate_route(i,problem)
    return a, b

ind1.fitness.values = evaluate(ind1,problem)
print ind1.fitness.valid
print ind1.fitness
