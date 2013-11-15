__author__ = 'Tomasz Godzik'

import math
import random

#what with depo?
def evaluate_route(route, problem):
    time = 0
    additional = 0
    current_cargo = problem.capacity
    current_x = problem.depotx
    current_y = problem.depoty
    for i in route:
        #check if we have enough cargo (check if possible - multiple goes?)
        if current_cargo > problem.customers[i].demand:
            #calculate the distance from one customer to another
            time += math.sqrt(
                math.pow(problem.customers[i].x - current_x, 2) + math.pow(problem.customers[i].y - current_y, 2))
        else:
            # cost of going back to customer
            time += math.sqrt(math.pow(problem.depotx - current_x, 2) + math.pow(problem.depoty - current_y, 2))
            time += math.sqrt(
                math.pow(problem.customers[i].x - problem.depotx, 2) + math.pow(problem.customers[i].y - problem.depoty,
                    2))
            current_cargo = problem.capacity

        #drop cargo
        current_cargo -= problem.customers[i].demand

        #change current location
        current_x = problem.customers[i].x
        current_y = problem.customers[i].y

        #if we have to wait
        time = max(time < problem.customers[i].ready, time)

        #if we are late, add penalty
        additional += max(0, (time - problem.customers[i].due) * 10)

        #time it takes to drop it
        time += problem.customers[i].service

    return time + additional

#wyliczamy wartosc fitness
def evaluate(individual, problem):
    a = len(individual)
    b = 0
    for i in individual:
        b += evaluate_route(i, problem)
    return a, b


def mutate_swap(ind):
    route1 = random.randint(0, len(ind) - 1)
    route2 = random.randint(0, len(ind) - 1)

    client1 = random.randint(0, len(ind[route1]) - 1)
    client2 = random.randint(0, len(ind[route2]) - 1)

    tmp = ind[route1][client1]
    ind[route1][client1] = ind[route2][client2]
    ind[route2][client2] = tmp

    return ind,


def mutate_inverse(ind):
    which = random.randint(0, len(ind) - 1)
    ind[which] = ind[which][::-1]
    return ind,


def mutate_insert(ind, max_vehicles):
    route = random.randint(0, len(ind) - 1)
    client = random.randint(0, len(ind[route]) - 1)
    found = ind[route][client]

    if random.random() < (1.0 / (2.0 * len(ind))) and len(ind) < max_vehicles:
        ind.append([found])
    else:
        new_route = random.randint(0, len(ind) - 1)
        place = random.randint(0, len(ind[new_route]))
        ind[new_route].insert(place, found)

    ind[route].remove(found)

    if len(ind[route]) == 0:
        ind.remove(ind[route])

    return ind,


def mutate_displace(ind,max_vehicles):
    route = random.randint(0, len(ind) - 1)
    rfrom = random.randint(0, len(ind[route]) - 1)
    rto = random.randint(rfrom + 1, len(ind[route]))
    subroute = ind[route][rfrom:rto]
    ind[route] = ind[route][0:rfrom] + (ind[route][rto:len(ind[route])])

    if random.random() < (1.0 / (2.0 * len(ind))) and len(ind) < max_vehicles:
        ind.append(subroute)
    else:
        new_route = random.randint(0, len(ind) - 1)
        place = random.randint(0, len(ind[new_route]))
        ind[new_route]=ind[new_route][0:place] + subroute + ind[new_route][place:len(ind[new_route])]

    if len(ind[route]) == 0:
        ind.remove(ind[route])
    return ind,

def mutate(ind,max_v,swap_rate=0.05,inverse_rate=0.1,insert_rate=0.05,displace_rate=0.15):
    if random.random() <= swap_rate:
        ind,= mutate_swap(ind)
    if random.random() <= inverse_rate:
        ind,= mutate_inverse(ind)
    if random.random() <= insert_rate:
        ind, = mutate_insert(ind,max_v)
    if random.random() <= displace_rate:
        ind, = mutate_displace(ind,max_v)
    return ind,

def cross_over(ind1,ind2):
    route = random.randint(0, len(ind1) - 1)
    rfrom = random.randint(0, len(ind1[route]) - 1)
    rto = random.randint(rfrom + 1, len(ind1[route]))
    subroute = ind1[route][rfrom:rto]
    # insert into the second one