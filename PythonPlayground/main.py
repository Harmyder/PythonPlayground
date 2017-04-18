import bspline

evaluator = bspline.loopData(bspline.withMemoFactory)

bspline.demo(evaluator)


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



