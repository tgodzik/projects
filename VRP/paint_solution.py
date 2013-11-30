__author__ = 'Tomasz Godzik'

from utils.paint import *
from utils.reader import *
import pickle

name = "C101.txt"

file_solution = open(name + ".solution")

hall = pickle.load(file_solution)

problem = from_file(["./solomon_25/" + name])[0]

draw_all(hall, problem)