import numpy as np
import pylab as pl

class BSpline:
    def __init__(self, knots, points, degree):
        self.knots_ = knots
        self.points_ = points
        self.degree_ = degree

    def getKnots(self): return self.knots_
    def getPoints(self): return self.points_
    def getDegree(self): return self.degree_

    def computePoint(self, t): raise NotImplementedError( "Should have implemented this" )

# recursive procedure without memoization
class BSplineWoMemo(BSpline):
    def __init__(self, knots, points, degree):
        super().__init__(knots, points, degree)

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
        pointsCount = self.points_.shape[1]
        for i in range(0, pointsCount):
            point = self.points_[0, i]
            b = self._basis(i, self.degree_+1, t)
            res += b * point
        return res

# more efficient version with memoization and exploiting of triangular structure for nonzero basis elements
class BSplineWithMemo(BSpline):
    # expects knot vector for clamped spline, so first and last (degree+1) elems are zeros
    def _findSpan(self, t):
        return np.searchsorted(self.knots_[self.degree_:self.knots_.size-self.degree_], t, side='right') + self.degree_ - 1

    def _computeBase(self, spanEnd, t):
        bases = np.zeros(self.degree_+1)
        bases[self.degree_] = 1.
        tcb = np.zeros(2) # two current bases from the next lower level
        for level in range(2, self.degree_+2):
            for minus in range(level):
                tcb[0], tcb[1] = tcb[1], tcb[0]
                tcb[1] = bases[self.degree_ - minus]
                i = spanEnd - minus
                left_denom =self. knots_[i+level-1] - self.knots_[i]
                left_numer = t - self.knots_[i]
                left = 0 if tcb[1] == 0 else tcb[1] * left_numer / left_denom
                right_denom = self.knots_[i+level] - self.knots_[i+1]
                right_numer = self.knots_[i+level] - t
                right = 0 if tcb[0] == 0 else tcb[0] * right_numer / right_denom
                bases[self.degree_-minus] = left + right
        return bases    

    def computePoint(self, t):
        spanEnd = self._findSpan(t)
        bases = self._computeBase(spanEnd, t)
        res = 0.
        start = spanEnd-self.degree_
        for i in range(start, start+self.degree_+1):
            point = self.points_[0, i]
            res += bases[i-start] * point
        return res

# factory functions
def woMemoFactory(knots, points, degree):
    return BSplineWoMemo(knots, points, degree)

def withMemoFactory(knots, points, degree):
    return BSplineWithMemo(knots, points, degree)

# helper function
def fill(evaluator, count):
    begin = evaluator.getKnots()[0]
    span = evaluator.getKnots()[-1] - begin
    step = float(span) / count
    res = []
    for i in range(0, count):
        x = begin + i * step
        res.append(evaluator.computePoint(x))
    res.append(evaluator.getPoints()[0, -1])
    return res

# data for different shapes
def twinHillsData(evaluatorFactory):
    degree = 3
    knots   = np.array([ 0, 0, 0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,13,13,13])
    knotsScale = knots[-1]
    knots = knots / knotsScale
    offsets = np.array([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15]) # x coordinates
    heights = np.array([ 1, 3, 2, 9, 9, 2, 3, 1, 1, 3, 2, 9, 9, 2, 3, 1]) # y coordinates
    points  = np.dstack((offsets, heights))
    return evaluatorFactory(knots, points, degree)

def loopData(evaluatorFactory):
    knots   = np.array([ 0, 0, 0, 0, 0.2, 0.4, 0.6, 0.8, 1, 1, 1, 1])
    offsets = np.array([ 0, 2, 4, 3,   1,   0,   2,   4])
    heights = np.array([ 1, 2, 4, 5,   5,   4,   2,   1])
    points  = np.dstack((offsets, heights))
    degree = 3
    return evaluatorFactory(knots, points, degree)

# compute and draw
def demo(evaluator):
    xy = fill(evaluator, 100)
    z = list(zip(*xy))
    points = evaluator.getPoints()
    points = points.swapaxes(1, 2)
    pl.plot(points[0][0], points[0][1], 'y')
    pl.scatter(z[0], z[1])
    pl.show()

# Usage example:
#
#import bspline
#evaluator = bspline.loopData(bspline.withMemoFactory)
#bspline.demo(evaluator)
