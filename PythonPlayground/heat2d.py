import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import Normalize
from matplotlib import cm
import matplotlib.animation as animation

# FTCS scheme for 2d heat equation

class Heat2d:
    def __init__(self, xLen, yLen, xStep, yStep, startData):
        self.xLen = xLen
        self.yLen = yLen
        self.xStep = xStep
        self.yStep = yStep
        self.u = startData
        self.unew = np.empty(shape=self.u.shape)


    def step(self, dT):
        u = self.u
        for i in range(1, self.xLen-1):
            for j in range(1, self.yLen-1):
                xPart = (u[i+1][j] - 2*u[i][j] + u[i-1][j]) / (self.xStep*self.xStep)
                yPart = (u[i][j+1] - 2*u[i][j] + u[i][j-1]) / (self.yStep*self.yStep)
                n = u[i][j] + dT*(xPart + yPart)
                self.unew[i][j] = n
        self.u[1:self.xLen-1][1:self.yLen-1] = self.unew[1:self.xLen-1][1:self.yLen-1].copy()

def draw_data(heat, norm):
    xx, yy = np.meshgrid(np.empty(heat.xLen), np.empty(heat.yLen))
    zz = np.empty(shape=xx.shape)
    for i in range(0, heat.xLen):
        for j in range(0, heat.yLen):
            xx[i,j] = i * heat.xStep
            yy[i,j] = j * heat.yStep
            zz[i,j] = heat.u[i][j]
    return xx, yy, zz

def demo():
    xLen = yLen = 5
    u = np.zeros(shape=(xLen, yLen))
    u[1][1] = 10
#    u[xLen//2][yLen//2] = 10
    norm = Normalize(vmin=0, vmax=100)
    heat = Heat2d(xLen, yLen, 1, 1, u)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    while True:
        for i in range(250): heat.step(0.0001)
        xx, yy, zz = draw_data(heat, norm)
        ax.plot_surface(xx, yy, zz, facecolors=cm.Greens(norm(zz)))
        fig.canvas.draw()
        plt.pause(0.1)

