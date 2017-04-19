import numpy as np
import pylab as pl

# recursive procedure without memoization
class BSpline:
    def __init__(self, knots, points, degree):
        self.knots_ = knots
        self.points_ = points
        self.degree_ = degree

    def getKnots(self): return self.knots_
    def getPoints(self): return self.points_
    def getDegree(self): return self.degree_

    def _basis(self, i, k, t):
        if k == 1:
            return 1 if (self.knots_[i] <= t and t < self.knots_[i+1]) else 0
        else:
            left_base = self._basis(i, k-1, t)
            left = 0 if left_base == 0 else left_base * float(t - self.knots_[i]) / (self.knots_[i+k-1] - self.knots_[i])
            right_base =  self._basis(i+1, k-1, t)
            right = 0 if right_base == 0 else right_base * float(self.knots_[i+k] - t) / (self.knots_[i+k] - self.knots_[i+1])
            return left + right

    def computePoint(self, t):
        res = 0.
        pointsCount = self.points_.shape[0]
        for i in range(0, pointsCount):
            point = self.points_[i]
            b = self._basis(i, self.degree_+1, t)
            res += b * point
        return res

# helper function
def fill(evaluator, count):
    begin = evaluator.getKnots()[0]
    span = evaluator.getKnots()[-1] - begin
    step = float(span) / count
    res = []
    for i in range(0, count):
        x = begin + i * step
        res.append(evaluator.computePoint(x))
    res.append(evaluator.getPoints()[-1])
    return res

# compute and draw
def demo(dataProvider):
    knots, points, degree = dataProvider()
    evaluator = BSpline(knots, points, degree)
    xy = fill(evaluator, 100)
    z = list(zip(*xy))
    points = evaluator.getPoints()
    points = points.swapaxes(0, 1)
    pl.plot(points[0], points[1], 'y')
    pl.scatter(z[0], z[1])
    pl.show()

# Usage example:

#import bsplineWoOptim as bspline
#
#def data():
#    ...
#    return knots, points, degree
#
#bspline.demo(data)
