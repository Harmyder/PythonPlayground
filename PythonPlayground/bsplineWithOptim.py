import numpy as np
import matplotlib.ticker as tck
import pylab as pl

# Efficient version with memoization and exploiting of triangular structure for nonzero basis elements
class BSplineBaseFuncs:
    def __init__(self, knots, degree):
        self.knots_ = knots
        self.degree_ = degree

    def getKnots(self): return self.knots_
    def getDegree(self): return self.degree_

    def getKnotsExtent(self): return self.knots_[-1] - self.knots_[0]

    # expects knot vector for clamped spline, so first and last (degree+1) elems are zeros
    def findSpan(self, t):
        # span [u_i, u_{i+1}] never riches its end, so for the last span we need to also handle u_{i+1}
        if (t == self.knots_[-1]):
            return self.knots_.size - self.degree_ - 2;
        return np.searchsorted(self.knots_[self.degree_:self.knots_.size-self.degree_], t, side='right') + self.degree_ - 1

    def computeBase(self, spanBack, t):
        bases = np.zeros(self.degree_+1)
        bases[self.degree_] = 1.
        tcb = np.zeros(2) # two current bases from the next lower level
        for level in range(2, self.degree_+2):
            for minus in range(level):
                tcb[0], tcb[1] = tcb[1], tcb[0]
                tcb[1] = bases[self.degree_ - minus]
                i = spanBack - minus
                left_denom =self. knots_[i+level-1] - self.knots_[i]
                left_numer = t - self.knots_[i]
                left = 0 if tcb[1] == 0 else tcb[1] * left_numer / left_denom
                right_denom = self.knots_[i+level] - self.knots_[i+1]
                right_numer = self.knots_[i+level] - t
                right = 0 if tcb[0] == 0 else tcb[0] * right_numer / right_denom
                bases[self.degree_-minus] = left + right
        return bases    

class BSpline(BSplineBaseFuncs):
    def __init__(self, knots, points, degree):
        super().__init__(knots, degree)
        self.points_ = points

    def getPoints(self): return self.points_

    def computePoint(self, t):
        spanBack = self.findSpan(t)
        bases = self.computeBase(spanBack, t)
        res = 0.
        start = spanBack-self.degree_
        for i in range(start, start+self.degree_+1):
            point = self.points_[i]
            res += bases[i-start] * point
        return res

class Span:
    def __init__(self, span, count):
        self.span = span
        self.count = count

# helper function
def fill(evaluator, count):
    begin = evaluator.getKnots()[0]
    step = float(evaluator.getKnotsExtent()) / count
    res = []
    spans = []
    for i in range(0, count+1):
        x = begin + i * step
        s = evaluator.findSpan(x)
        if len(spans) > 0 and spans[-1].span == s:
            spans[-1].count += 1
        else:
            spans.append(Span(s, 1))
        res.append(evaluator.computePoint(x))
    return res, spans

# Usage example
#def data(): ... return knots, points, degree
#.demo(data)
def demo(dataProvider):
    knots, points, degree = dataProvider()
    evaluator = BSpline(knots, points, degree)
    xy, spans = fill(evaluator, 100)
    z = list(zip(*xy))
    points = evaluator.getPoints()
    points = points.swapaxes(0, 1)
    pl.plot(points[0], points[1], 'y')
    currentIndex = 0
    for s in spans:
        nextIndex = currentIndex+s.count
        pl.scatter(z[0][currentIndex:nextIndex], z[1][currentIndex:nextIndex])
        currentIndex = nextIndex
    pl.show()


# Usage example
#knots = np.array([ 0, 0, 0, 1, 1, 2, 2, 2])
#.demoBases(knots, 2)
def demoBases(knots, degree):
    assert(degree > 0)
    points = np.zeros((knots.size-degree-1, 2))
    evaluator = BSpline(knots, points, degree)
    firstNotEmptySpan = 0
    pointsPerSpan = 200
    bases = [[[] for _ in range(2)] for _ in range(knots.size-degree-firstNotEmptySpan)]
    for spanBack in range(firstNotEmptySpan, knots.size-degree-1):

        for t in range(0, pointsPerSpan):
            x = knots[spanBack] + (knots[spanBack + 1] - knots[spanBack]) * float(t) / pointsPerSpan
            localBases = evaluator.computeBase(spanBack, x)
            bStart, bStop = spanBack - degree, spanBack + 1
            for b in range(bStart, bStop):
                if b >= firstNotEmptySpan:
                    bases[b - firstNotEmptySpan][0].append(x)
                    bases[b - firstNotEmptySpan][1].append(localBases[b - bStart])

    f, ax = pl.subplots()
    ax.minorticks_on()
    ticks = knots[degree:knots.size-degree]
    ax.set_xticks(ticks)

    for b in bases:
        ax.plot(b[0], b[1])
    pl.show()

def demoBasesEquidistant(step, degree):
    knots = np.concatenate((np.zeros(degree), (np.arange(1/step)*step), np.ones(degree+1)))
    demoBases(knots, degree)

