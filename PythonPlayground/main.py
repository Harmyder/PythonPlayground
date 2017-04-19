import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt

import bsplineWithOptim as bspline

# data for different shapes
def twinHillsData():
    degree = 3
    knots   = np.array([ 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,13,13,13])
    knotsScale = knots[-1]
    knots = knots / knotsScale
    offsets = np.array([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]) # x coordinates
    heights = np.array([ 1, 3, 2, 9, 9, 2, 3, 1, 1, 3, 2, 9, 9, 2, 3, 1]) # y coordinates
    points  = np.dstack((offsets, heights))
    return knots, points[0], degree

def loopData():
    knots   = np.array([ 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1, 1, 1])
    offsets = np.array([ 0, 2, 4, 3,   1,   0,   2,   4])
    heights = np.array([ 1, 2, 4, 5,   5,   4,   2,   1])
    points  = np.dstack((offsets, heights))
    degree = 3
    return knots, points[0], degree




#knots = np.array([ 0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5])
knots = np.array([0, 0, 0, 0, 1, 2, 2, 2, 3, 3, 3, 3])
bspline.demoBases(knots, 2)

#def basisFuns1():
#    gray = '#eeeeee'
#    for i in range(knots.size - 1):
#        if (knots[i] != knots[i+1]):
#            label = '$N_{{{},0}}$'.format(i)
#            pl.plot([knots[i], knots[i+1]], [1, 1], '-', label=label)
#            pl.plot([knots[i], knots[i]], [0, 1], color=gray, linestyle='--')
#    pl.plot([knots[-1], knots[-1]], [0, 1], color=gray, linestyle='--')
#    pl.legend()

#basisFuns1()
#pl.show()



