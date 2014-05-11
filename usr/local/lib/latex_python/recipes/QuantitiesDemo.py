from Quantities import Cup, Quart, FluidOunce, Teaspoon
from fractions import Fraction

def show(quantity):
    print
    print '--- %s %s ---' % (quantity.quantity, quantity.plural)
    print 'brief: %s' % str(quantity)
    print 'full:  %s' % quantity.fullString()

show(Cup(1))
show(Cup('1/2'))
show(Cup('1/16'))
show(Cup('2/3'))
show(Cup('1 1/2'))
show(Cup(8))
show(Cup(13))
show(FluidOunce(300))
# todo partial (1/2 c)
show(FluidOunce(1300))
show(Teaspoon(300))
show(Teaspoon(1300))

show(Teaspoon(3) * 3.5)

