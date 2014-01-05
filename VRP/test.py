from utils.reader import *
from utils import evaluate_route

name = "C101.txt"
#770.353178717 1391.68351644 8.0
pathes = [[20, 24, 25, 19, 9, 12, 23, 22, 21], [13, 17, 18, 10, 11, 14, 6, 4, 2, 1], [5, 3, 7, 8, 15, 16]]
file_solution = open(name + ".solution")

problem = from_file(["./solomon/" + name])[0]

for p in pathes:
    print evaluate_route(p,problem, penalty_cost=100000)