#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe
from latex_python.recipes.Quantities import Cup, FluidOunce, Tablespoon, Teaspoon, Bunch

def generate():
    r = Recipe('Cuban Beans and Rice')

    r.ingredient('olive oil', Tablespoon(3))
    r.ingredient('onion', 1, 'peeled and chopped')
    r.ingredient('carrot', 1, 'in 1/4-inch slices')
    r.ingredient('garlic', 4, 'minced')
    r.ingredient('short grain brown rice', Cup(0.75))

    r.ingredientGroupDivider()
    r.ingredient('water', Cup(3), 'about 1/3 less if using white rice')
    r.ingredient('dry black beans', Cup(1), 'washed and soaked for 2+ hours')

    r.ingredient('salt', Teaspoon(1))
    r.ingredient('black pepper', Teaspoon(0.25))
    r.ingredient('ground cumin', Teaspoon(1), 'or more to taste')
    r.ingredient('cayenne', Teaspoon(0.25))

    # option 3 (Danni's)
    r.ingredient('bay leaves', 1)
    r.ingredient('coriander', Teaspoon(0.5))
    r.ingredient('\\emph{smoked} red pepper flakes', Teaspoon(1))
    r.ingredient('cilantro', Cup(0.25), 'chopped, including stems')

    r.ingredientGroupDivider()
    r.ingredient('red bell pepper', 0.5, 'cut into chunks')
    r.ingredient('lime (juice of)', 1)

    r.doubleRecipe()


    r.description('Inspired by the Swiss pressure cooking cookbook, revised by Danni')

    r.addInstruction('''
        Heat olive oil over medium high heat in pressure cooker.
        Add onion, garlic, and carrot if you are including one. Sautée until onion softens.
        Add rice over high heat, stirring often, until lightly golden.

        Add water and soaked, drained beans. Stir in salt, pepper, herbs, and spices.
        Close lid and bring pressure to first ring over high heat.
        Cook for 22 minutes on the first ring.

        Use the natural release method.
        When the pressure releases, add the red bell pepper chunks and the lime juice.
    ''')
    r.addInstruction('Serve with plain yogurt.')

    r.yieldPerBatch(4, 'servings')

    return r.generate('cubanBeansAndRice.pdf')

if __name__ == '__main__':
    generate()

