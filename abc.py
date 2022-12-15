from PIL import Image
import numpy as np
import random
from matplotlib import pyplot as plt

image = Image.open('image.png')
print(image.format)
print(image.size)
print(image.mode)
image = image.convert('L')
image = image.resize((100,100))
image.show()
#print(image.format)
#print(image.size)
#print(image.mode)

DEBUG = False

def debug(str):
    if DEBUG:
        print(str)

def get_source():
    image = Image.open('image.png')
    image = image.convert('L')
    image = image.resize((100,100))
    source = np.array(image)
    return source

#objective function = sum of all values in the row

def objective_function(array):
    objective_function_array = np.sum(array,axis=1)                     #axis = 1 so that it calculates the sum of the array row wise.
                                                                        #eg: a = np.sum([[0.5, 0.7, 0.2, 1.5],[0.5, 0.7, 0.2, 1.5]],axis=1)
    return objective_function_array

def __generate_pi():
    return random.uniform(0, 1)

def __individual_objective_function_and_fitness(array):
    objective_score = np.sum(array)
    if objective_score >=0:
        fitness_score = 1/(1 + objective_score)
    else:
        fitness_score = 1 + objective_score
    return objective_score, fitness_score

def create_trail_array(length):
    return np.zeros(length)

def fitness_function(array):
    fitness_function_array = []
    for value in array:
        if value >= 0:
            fitness_function_array.append(1/(1 + value))
        else:
            fitness_function_array.append(1+value)
    return fitness_function_array

def __choose_random_number():
    return np.random.randint(1,100)

def __employed_bee_phase(source, objective_function_array, fitness_function_array, trail):
    for bee in range (len(objective_function_array)):
        random_varaible = __choose_random_number()
        random_partner = __choose_random_number()
        fi = __generate_pi()
        bee_current_array = []
        bee_current_array = source[bee]
        source_new = (source[bee][random_varaible]) + (fi * (source[bee][random_varaible]-source[random_partner][random_varaible]))
        debug("Employed bee phase: Bee No. {} and the modified value {}".format(bee, source_new))
        debug(source_new)
        bee_current_array[random_varaible] = source_new
        objective_instance, fitness = __individual_objective_function_and_fitness(bee_current_array)
        if (fitness < fitness_function_array[bee]):
            source[bee][random_varaible] = source_new
            objective_function_array[bee] = objective_instance
            fitness_function_array[bee] = fitness
            trail[bee] = 0
        else:
            trail[bee] += 1

    return source, objective_function_array, fitness_function_array, trail

def __Onlooker_bee_phase(source, objective_function_array, fitness_function_array, trail, fitness_probability):
    for onlooker_bee in range(len(objective_function_array)):
        random_number = __generate_pi()
        if (random_number<fitness_probability[onlooker_bee]):
            random_varaible = __choose_random_number()
            random_partner = __choose_random_number()
            fi = __generate_pi()
            bee_current_array = []
            bee_current_array = source[onlooker_bee]
            source_new = (source[onlooker_bee][random_varaible]) + (fi * (source[onlooker_bee][random_varaible]-source[random_partner][random_varaible]))
            debug("Onlooker bee phase: Bee No. {} and the modified value {}".format(onlooker_bee, source_new))
            debug(source_new)
            bee_current_array[random_varaible] = source_new
            objective_instance, fitness = __individual_objective_function_and_fitness(bee_current_array)
            if (fitness < fitness_function_array[onlooker_bee]):
                source[onlooker_bee][random_varaible] = source_new
                objective_function_array[onlooker_bee] = objective_instance
                fitness_function_array[onlooker_bee] = fitness
                trail[onlooker_bee] = 0
            else:
                trail[onlooker_bee] += 1
        
        else:
            continue
    return source, objective_function_array, fitness_function_array, trail

def __generate_new_source__():
    return np.random.randint(0,100, size=(100))

def __onlooker_bee_phase_fitness_probability__(fitness_array):
    probability_array = []
    for individual_fitness in range (len(fitness_array)):
        probability_array.append(individual_fitness/len(fitness_array))
    return probability_array

def __scout_bee_phase(source, objective_function_array, fitness_function_array, trail, __scout_bee_limit__):
    for scout_bee in range(len(trail)):
        if (trail[scout_bee]>__scout_bee_limit__):
            source[scout_bee] = __generate_new_source__()
            objective_function_array[scout_bee], fitness_function_array[scout_bee] = __individual_objective_function_and_fitness(source[scout_bee])
            trail[scout_bee] = 0
        else:
            continue

    return source, objective_function_array, fitness_function_array, trail


def main():
    for i in range (20):
        __scout_bee_limit__ = 1
        source  = get_source()
        #source = source.setflags(write=1)
        debug("The source array is:")
        debug(source)

        #Employed bee phase
        objective_function_array = objective_function(source)
        debug("The objective function array is:")
        debug(objective_function_array)

        fitness_function_array = fitness_function(objective_function_array)
        debug("The initial fitness function is")
        debug(fitness_function_array)

        trail = create_trail_array(len(objective_function_array))
        debug("The initial trail array: ")
        debug(trail)

        source, objective_function_array, fitness_function_array, trail = __employed_bee_phase(source, objective_function_array, fitness_function_array, trail)
        debug("The objective function array after employed bee phase is:")
        debug(objective_function_array)

        debug("The fitness function after employeed bee phase is")
        debug(fitness_function_array)

        debug("The trail array after employeed bee phase: ")
        debug(trail)

        #Onlooker bee phase
        fitness_probability = __onlooker_bee_phase_fitness_probability__(fitness_function_array)
        source, objective_function_array, fitness_function_array, trail = __Onlooker_bee_phase(source, objective_function_array, fitness_function_array, trail, fitness_probability)
        debug("The objective function array after Onlooker bee phase is:")
        debug(objective_function_array)

        debug("The fitness function after onlooker bee phase is")
        debug(fitness_function_array)

        debug("The trail array after onlooker bee phase: ")
        debug(trail)

        #Scout bee phase
        source, objective_function_array, fitness_function_array, trail = __scout_bee_phase(source, objective_function_array, fitness_function_array, trail, __scout_bee_limit__)
    img = Image.fromarray(source)
    img = img.convert("RGB")
    img.save('my.png')
    img.show()
    
main()