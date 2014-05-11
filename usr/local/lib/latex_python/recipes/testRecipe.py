from Recipe import Recipe
from Quantities import Cup

r = Recipe('Crepes')

r.doubleRecipe()
r.tripleRecipe()

r.ingredient('Flour',
             Cup(1),
             'in order of preference: pastry, white whole wheat, bread')
r.ingredient('Eggs', 3)
r.ingredient('Milk',
             Cup(0.25),
             'mix in some buttermilk or kefir for flavor')

r.description('''
French style crepes, which are very good with either sweet or savory ingredients.
''')

r.instructions('''
Mix all the ingredients thouroughly in a blender...
''')

r.yieldPerBatch(10, 'crepes')

r.generate('crepes.pdf')

