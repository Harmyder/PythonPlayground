import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import bsplineWithOptim as bspline
from matplotlib import cm

class bsplineSurface(object):
    def __init__(self, uKnots, vKnots, points, degree):
        self.uBasis = bspline.BSplineBaseFuncs(uKnots, degree)
        self.vBasis = bspline.BSplineBaseFuncs(vKnots, degree)
        self.points_ = points
        self.degree_ = degree

    def getUKnotsExtent(self): return self.uBasis.getKnotsExtent()
    def getVKnotsExtent(self): return self.vBasis.getKnotsExtent()
    def getUKnotsBegin(self): return self.uBasis.getKnots()[0]
    def getVKnotsBegin(self): return self.vBasis.getKnots()[0]

    def computePoint(self, u, v):
        uSpanBack = self.uBasis.findSpan(u)
        uBases = self.uBasis.computeBase(uSpanBack, u)
        vSpanBack = self.vBasis.findSpan(v)
        vBases = self.vBasis.computeBase(vSpanBack, v)
        res = 0.
        uStart = uSpanBack-self.degree_
        vStart = vSpanBack-self.degree_
        for i in range(uStart, uStart+self.degree_+1):
            for j in range(vStart, vStart+self.degree_+1):
                point = self.points_[i][j]
                res += uBases[i-uStart] * vBases[j-vStart] * point
        return res

def fill(evaluator, uCount, vCount):
    uBegin = evaluator.getUKnotsBegin()
    vBegin = evaluator.getVKnotsBegin()
    uStep = evaluator.getUKnotsExtent() / uCount;
    vStep = evaluator.getVKnotsExtent() / vCount;
    xx, yy = np.meshgrid(np.empty(uCount+1), np.empty(vCount+1))
    zz = np.empty(shape=xx.shape)
    for i in range(0, uCount + 1):
        for j in range(0, vCount + 1):
            u = uBegin + i * uStep
            v = vBegin + j * vStep
            p = evaluator.computePoint(u, v)
            xx[i,j] = p[0]
            yy[i,j] = p[1]
            zz[i,j] = p[2]
    return xx, yy, zz

def hillsData():
    uKnots = np.array([0,0,0,0,1,2,3,4,4,4,4])
    vKnots = np.copy(uKnots)
    side = 7
    points = np.empty(shape=(side,side,3))
    for i in range(0,side):
        for j in range(0,side):
            points[i][j] = np.array([i,j,0])
    points[side//2][1][2] = 1
    points[side//2][side-2][2] = 1.5
    points[1][side//2][2] = 2
    points[side-2][side//2][2] = 2.5
    return uKnots, vKnots, points, 3

def demo():
    evaluator = bsplineSurface(*hillsData())
    xx, yy, zz = fill(evaluator, 30, 30)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(xx, yy, zz, facecolors=cm.Greens(zz / zz.max()))
    plt.show()
