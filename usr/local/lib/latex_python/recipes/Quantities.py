# /usr/bin/env python

from fractions import Fraction

class Quantity:
    'a class representing a number of teaspoons, tablespoons, cups, quarts, etc.'
    nextSizeClass = None  # class of the next measurement unit: t > T > Cup > quart, etc.
    nextSizeMultiple = 0
    abbreviation = ''
    singular = ''
    plural = ''

    def __init__(self, quantity, qualifier='', smartScaling=True):
        # how many cups, etc?
        # set this using decimal, float, or string.
        # you can also use tuple(n,m), where n and m are decimal, float, or string.
        if isinstance(quantity, (tuple, list, set)):
            self.quantity = (self.parseQuantityParameter(quantity[0]),
                             self.parseQuantityParameter(quantity[1]))
        else:
            self.quantity = self.parseQuantityParameter(quantity)

        # self.qualifier is like 'large' or 'overflowing' to specify
        # '1 large bunch', '2 large bunches', '1 overflowing cup', etc
        self.qualifier = qualifier
        
        # if True, then (q * x), (q + x), and __init__ will auto-group the units
        # i.e. Cup > Quart, etc
        self.smartScaling = smartScaling

    def parseQuantityParameter(self, quantity):
        # Strings can be '1/2', '1', '0.5', '.5', '1 5/8', etc.
        # (it's technically possible even to say '1 2 3/4' to mean 3.75)
        quantityStrings = str(quantity).split(' ')  # turn '1 5/8' into ['1', '5/8']
        result = 0
        for q in quantityStrings:
            if q.strip() != '':  # might happen with double spacing
                result += Fraction(q)
        return result

    # 'other' must be scalar (not tuple)
    def __add__(self, other):
        if isinstance(self.quantity, tuple):
            newQuantity = (self.quantity[0] + other,
                           self.quantity[1] + other)
        else:
            newQuantity = self.quantity + other
        result = self.__class__(newQuantity, qualifier=self.qualifier, smartScaling=self.smartScaling)
        return result

    # 'other' must be scalar (not tuple)
    def __mul__(self, other):
        if isinstance(self.quantity, tuple):
            newQuantity = (self.quantity[0] * other,
                           self.quantity[1] * other)
        else:
            newQuantity = self.quantity * other
        result = self.__class__(newQuantity, qualifier=self.qualifier, smartScaling=self.smartScaling)
        return result

    def resolveQuantity(self):
        '''
        return a list of Quantity objects representing this quantity, such that:
        - no quantity contains a fraction, except the native one (i.e. the zero-level of recursion)
        - all members of the list are in descending categorical scale - [Quart, Cup, Tablespoon, ...]
        '''
        if not self.smartScaling:
            # don't auto-group anything
            return [self]
        if isinstance(self.quantity, tuple):
            if self.quantity[0] >= self.nextSizeMultiple and self.nextSizeClass is not None:
                nextQuantity = (int(self.quantity[0] / self.nextSizeMultiple),
                                int(self.quantity[1] / self.nextSizeMultiple))
                remainder = (self.quantity[0] - (nextQuantity * self.nextSizeMultiple),
                             self.quantity[1] - (nextQuantity * self.nextSizeMultiple))
                nextMeasurement = self.nextSizeClass(nextQuantity)
                result = nextMeasurement.resolveQuantity()
                if remainder[0] > 0 or remainder[1] > 0:
                    result.append(self.__class__(remainder))
                return result
            else:
                return [self]
        else:
            if self.quantity >= self.nextSizeMultiple and self.nextSizeClass is not None:
                nextQuantity = int(self.quantity / self.nextSizeMultiple)
                remainder = self.quantity - (nextQuantity * self.nextSizeMultiple)
                nextMeasurement = self.nextSizeClass(nextQuantity)
                result = nextMeasurement.resolveQuantity()
                if remainder > 0:
                    result.append(self.__class__(remainder))
                return result
            else:
                return [self]

    def fullString(self):
        resolved = self.resolveQuantity()
        result = []
        for q in resolved:
            if q.quantity <= 1:
                name = q.singular
            else:
                name = q.plural
            result.append('%s %s %s' % (q.fractionString(), self.qualifier, name))
        return ' and '.join(result)

    def __str__(self):
        resolved = self.resolveQuantity()
        result = []
        for q in resolved:
            result.append(q.fractionString() + q.abbreviation)
        return ' + '.join(result)

    def fractionString(self):
        if isinstance(self.quantity, tuple):
            quantityRange = self.quantity
        else:
            quantityRange = [self.quantity]

        result = []
        for q in quantityRange:
            description = []
            # split the 13/8 back out into 1 5/8
            wholeNumber = int(q)
            remainder = q - wholeNumber
            if wholeNumber != 0:
                description.append(str(wholeNumber))
            if remainder != 0:
                description.append(str(remainder))
            result.append(' '.join(description))
        return '-'.join(result)  # e.g. 1-2 cups

class Can(Quantity):
    nextSizeClass = None
    abbreviation = 'can'
    singular = 'can'
    plural = 'cans'

class Quart(Quantity):
    nextSizeClass = None
    abbreviation = 'qt'
    singular = 'quart'
    plural = 'quarts'

class Cup(Quantity):
    nextSizeClass = Quart
    nextSizeMultiple = 4
    abbreviation = 'c'
    singular = 'cup'
    plural = 'cups'

class Tablespoon(Quantity):
    nextSizeClass = Cup
    nextSizeMultiple = 16
    abbreviation = 'Tbsp'
    singular = 'Tablespoon'
    plural = 'Tablespoons'

class Teaspoon(Quantity):
    nextSizeClass = Tablespoon
    nextSizeMultiple = 3
    abbreviation = 'tsp'
    singular = 'teaspoon'
    plural = 'teaspoons'

class FluidOunce(Quantity):
    nextSizeClass = Cup
    nextSizeMultiple = 16
    abbreviation = 'fl.oz'
    singular = 'fluid ounce'
    plural = 'fluid ounces'

class Pound(Quantity):
    nextSizeClass = None
    abbreviation = 'lb'
    singular = 'pound'
    plural = 'pounds'

class Ounce(Quantity):
    nextSizeClass = Pound
    nextSizeMultiple = 16
    abbreviation = 'oz'
    singular = 'ounce'
    plural = 'ounces'

class Bunch(Quantity):
    nextSizeClass = None
    abbreviation = 'bunch'
    singular = 'bunch'
    plural = 'bunches'
