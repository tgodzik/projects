import pygame
from pygame.locals import *
import random




def draw_route(route,problem,screen):
    color= random.randint(20,255),random.randint(20,255),random.randint(20,255)
    current_cargo = problem.capacity
    current_x = problem.depotx
    current_y = problem.depoty
    for i in route:
        if current_cargo > problem.customers[i].demand:
            pygame.draw.line(screen,color,(5*problem.customers[i].x,5*problem.customers[i].y),(5*current_x,5*current_y),2)
        else:
            pygame.draw.line(screen,color,(5*problem.depotx,5*problem.depoty),(5*current_x,5*current_y),2)
            pygame.draw.line(screen,color,(5*problem.depotx,5*problem.depoty),(5*problem.customers[i].x,5*problem.customers[i].y),2)
            current_cargo = problem.capacity

        #drop cargo
        current_cargo -= problem.customers[i].demand

        #change current location
        current_x = problem.customers[i].x
        current_y = problem.customers[i].y


    pygame.draw.line(screen,color,(5*problem.depotx,5*problem.depoty),(5*current_x,5*current_y),2)

def draw_instance(ind,problem):
    pygame.init()
    size = width, height = 500, 500
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Visualization")
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (0,0,0), (5*problem.depotx,5*problem.depoty), 5, 5)
    for r in ind:
        draw_route(r,problem,screen)
    pygame.display.flip()
    while pygame.event.wait().type != KEYDOWN: pass



def draw_all(hall,problem):
    for i in hall:
        draw_instance(i,problem)







