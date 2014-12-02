#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe, Ingredient
from latex_python.recipes.Quantities import Quart, Cup, Tablespoon, Teaspoon, FluidOunce, Bunch, Pound, Ounce

from os.path import splitext

# title of the dish
recipe = Recipe('Title')

# Description shows up near the title.
recipe.description('An enticing sentence that makes you want to cook this.')

# ingredient name, quantity, prep/notes
#
# Quantities:
# use Cup((2,3)) to indicate a range
# use quantity == None for things like salt (i.e. to taste)
#
# Descriptions:
# Quantities can have a descriptive modifier like 'large' or 'overflowing'.
# (there is no restriction on what can be identified)
# EX:   recipe.ingredient('brown rice', Cup(1.5, 'overflowing'))
#       recipe.ingredient('kale', Bunch(1, 'large'), 'chopped')
recipe.ingredient('apples', 3, 'galas, preferably')
recipe.ingredient('bosc pears', 2)

recipe.ingredientSpace() # to add white space
recipe.ingredient('salt', None, 'to taste')

recipe.ingredientSection('Topping') # to have a titled ingredient section
# all subsequent calls to ingredient() will be added to the "current" section ('Topping' in this case)
recipe.ingredient('chocolate chips', None, 'a handful should do')


recipe.paragraph('''
    A paragraph of instructions. Add as many as you like.
''')

# yield: either (amount) or (amount, description)
# recipe.yieldPerBatch(10, 'crepes')
recipe.yieldPerBatch(FluidOunce(80))


# prints additional "quantity" columns and yield amounts
# recipe.double()
# recipe.triple()
# recipe.quadrouple()

if __name__ == '__main__':
    recipe.generate(splitext(__file__)[0] + '.pdf')
