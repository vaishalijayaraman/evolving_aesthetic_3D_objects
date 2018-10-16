#HEADERS FOR ALGORITHM
import os
import subprocess

import numpy as np
import array as a
import math as mm
import random
import re

from deap import algorithms
from deap import base
from deap import creator
from deap import tools

tmp_file = "tmp.txt"

blender = "/Applications/blender.app/Contents/MacOS/blender"
formObjectAndgetVerticespy = "/Applications/blender.app/Contents/MacOS/formObjectAndgetVertices.py"

command_to_run = '%s --background --python %s' % (blender, formObjectAndgetVerticespy)
#command_to_run = '%s --python %s' % (blender, formObjectAndgetVerticespy)

#FUNCTIONS
def distance(p,q):
    total = 0
    for i in range(len(p)):
        total = total + (abs(p[i][0]-q[i][0])) + (abs(p[i][1]-q[i][1]))
    return total


def pointify(v,p):
    #p is the values of the start object that aren't getting optimized
    p = [[-1,0],[0,0],[1,0]]
    for i in range(0,number_of_points_optimize):
        k = positions_of_points_optimize[i] - 1
        p.insert(k,[])
        p[k].insert(0,(v[(2*i)-2]))
        p[k].insert(1,(v[(2*i)-1]))    
    return p


stop_coords = [[-1,0,1],[0,0,1],[2,2,1],[1,0,1]]

length = len(stop_coords)

start_coords = [[-1,0,1],[0,0,1],[0,0,1],[1,0,1]]

#number of points in the START OBJECT
number_of_points_total = 4
#nuber of points the program should optimize
number_of_points_optimize = 2
#which of these points should it optimize
positions_of_points_optimize = [3]
#how many coordinates does each point have?
number_of_variables = 2
#the total number of values the program has to optimize
number_of_variables_total = number_of_variables * number_of_points_optimize

points = []
points_new = points
fitness_val = 0

# PROBLEM INFO
# Start: [[-1,0,0],[0,0,0],[0,0,0],[1,0,0]]
# Target: [[-1,0,0],[0,0,0],[2,2,0],[1,0,0]]
# The individual now is an array of two ints between 0 and 2, randomly generated.


int numOfVars = 12;

for i in range():


    creator.create("FitnessMax", base.Fitness, weights=(-1.0,))
    #creator.create("Individual", a.array, typecode='f', fitness=creator.FitnessMax)
    #creator.create("Individual", list, fitness=creator.FitnessMax)
    creator.create("Individual", np.ndarray, fitness=creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("attr_bool", random.uniform, 0, 2)
    toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, 2) #ind_size
    toolbox.register("population", tools.initRepeat, list, toolbox.individual, n=10)

    def evalFitness(individual):
        try:
            print("the numbers: ", individual[0], individual[1])
            with open(tmp_file, "w") as f:
            #f.write("%d" % individual[0])
                f.write("%.2d" % individual[0])
                f.write(",")
            #f.write("%d" % individual[1])
                f.write("%.2d" % individual[1])
            #for i in range(1,len(individual)):
                #for j in range(2):
                    #f.write(",")
                    #f.write("%d" % individual[i][j])          
            f.close()
        
            fit = subprocess.check_output(command_to_run, shell=True)
        
            blenderBlah = '\nfound bundled python: /Applications/blender.app/Contents/MacOS/../Resources/2.77/python\n\nBlender quit\n'
            if blenderBlah in fit:
                b = fit.replace(blenderBlah, '')

            fitval = float(b)
            return (fitval,)
        
            #return(individual[0]+individual[1],)

        except Exception as e:
         #pass
            print("something is wrong")

    toolbox.register("evaluate", evalFitness)
    toolbox.register("mate", tools.cxTwoPoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
    toolbox.register("select", tools.selTournament, tournsize=3)

    if __name__ == "__main__":
        pop = toolbox.population(n=30)
        algorithms.eaSimple(pop, toolbox, cxpb=0.5, mutpb=0.2, ngen=2)
        print(tools.selBest(pop, k=1)[0])

