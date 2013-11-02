__author__ = 'Tomasz Godzik'

import math

#what with depo?
def evaluate_route(route,problem):
    time=0
    additional=0
    current_cargo=problem.capacity
    current_x=problem.depotx
    current_y=problem.depoty
    for i in route:
        #check if we have enough cargo (check if possible - multiple goes?)
        if current_cargo > problem.customers[i].demand:
            #calculate the distance from one customer to another
            time+=math.sqrt(math.pow(problem.customers[i].x-current_x,2)+math.pow(problem.customers[i].y-current_y,2))
        else:
            # cost of going back to customer
            time+=math.sqrt(math.pow(problem.depotx-current_x,2)+math.pow(problem.depoty-current_y,2))
            time+=math.sqrt(math.pow(problem.customers[i].x-problem.depotx,2)+math.pow(problem.customers[i].y-problem.depoty,2))
            current_cargo=problem.capacity

        #drop cargo
        current_cargo-=problem.customers[i].demand

        #change current location
        current_x=problem.customers[i].x
        current_y=problem.customers[i].y

        #if we have to wait
        time=max(time<problem.customers[i].ready, time)

        #if we are late, add penalty
        additional += max(0, (time - problem.customers[i].due)*10 )

        #time it takes to drop it
        time+=problem.customers[i].service

    return time+additional

#wyliczamy wartosc fitness
def evaluate(individual,problem):
    a =  len(individual)
    b=0
    for i in individual:
        b+=evaluate_route(i,problem)
    return a, b