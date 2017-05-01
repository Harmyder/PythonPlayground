import numpy as np
import matplotlib.pyplot as plt

def epsTest():
    n = 1000
    xExtent = (-1.5, 0.5)
    yExtent = (-1.0, 1.0)
    x = np.linspace(*xExtent, n)
    y = np.linspace(*yExtent, n)
    z0 = np.repeat(x[np.newaxis], n, axis=0) + 1j * np.repeat(y[np.newaxis], n, axis=0).transpose()
    z = np.zeros(shape=(n,n))
    c = np.zeros(shape=(n,n))

    depth = 32;
    for k in range(depth):
        z = np.square(z) + z0
        c[abs(z) < 2] = k # in case of NaN or infty warning is raised
    
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.set_aspect('equal')
    plt.imshow(c, interpolation='nearest', cmap=plt.cm.ocean, extent=(*xExtent, *yExtent))
    plt.colorbar()
    plt.savefig("test.eps", format="eps")
    plt.show()

