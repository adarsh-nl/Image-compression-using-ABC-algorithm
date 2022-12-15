# Image-compression-using-ABC-algorithm

# About Artificial Bee colony Algorithm.
In computer science and operations research, the artificial bee colony algorithm (ABC) is an optimization algorithm based on the intelligent foraging behaviour of honey bee swarm, proposed by Derviş Karaboğa in 2005.

# Image compression using ABC algorithm
This is a compression of image with few loss of data. A random image has been selected and fed in to the algorithm. Initially, the image is converted to gray scale and then resized to shape of 100 X 100. 

This image array is considered as the food source for all the three bee phases.
1. Employed bee phase
2. On-looker bee phase
3. Scout bee phase

Objective function is: Sum of all the values in the row (i.e., x1+x2+x3+......+x100). This code is implemented with out any constraints, It may be modified to work with constraints in the future.

Fitness function: 1/(1+value) if value is > 0. Else just 1+value.

Probability of fitness: value/sum (fitness_array)

#Required libraries.
Pillow
Numpy
Random
