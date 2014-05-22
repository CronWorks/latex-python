#!/usr/bin/env python

from latex_python.recipes.Recipe import Recipe
from latex_python.recipes.Quantities import Cup

recipe = Recipe('Crepes')

recipe.doubleRecipe()
recipe.tripleRecipe()

recipe.ingredient('Flour', Cup(1), 'in order of preference: whole wheat pastry, white whole wheat, bread')
recipe.ingredient('Eggs', 3)
recipe.ingredient('Milk', Cup(1.25), 'mix in some buttermilk or kefir for flavor')

recipe.description('French style crepes, which are very good with either sweet or savory ingredients.')

# note: should covert 1/3 to \nicefrac{1}{3}
recipe.addInstruction('''
Mix all the ingredients thouroughly with a hand mixer (preferred), or in a blender
until you get a uniform batter with the consistency of cream. After mixing,
let it sit about 10 minutes and add milk as necessary (if it thickens).
Pour about 1/3 cup batter in an evenly-heated flat pan, after a small amount of
butter has been melted in it.

Cook the first side until it smells like bread,
and the second side only for about 10 seconds.
''')

recipe.yieldPerBatch(10, 'crepes')

if __name__ == '__main__':
    recipe.generate()
