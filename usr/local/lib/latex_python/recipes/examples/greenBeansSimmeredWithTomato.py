#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe
from latex_python.recipes.Quantities import Cup, FluidOunce, Tablespoon, Teaspoon, Bunch, Pound


def generate():
    # title of the dish
    r = Recipe('Green Beans Simmered with Tomato')

    # Description shows up near the title.
    r.description('The tomato disintegrates and turns into a sauce for the beans')

    # ingredient name, quantity, prep/notes
    # NOTE: Quantities can have a descriptive modifier like 'large' or 'overflowing'.
    #       (there is no restriction on what can be identified)
    # EX:   r.ingredient('brown rice', Cup(1.5, 'overflowing'))
    #       r.ingredient('kale', Bunch(1, 'large'), 'chopped')
    r.ingredient('olive oil', Tablespoon(2))
    r.ingredient('small white onions', 2, 'sliced into thin rounds')
    r.ingredient('carrot', 1, 'sliced into thin rounds')
    r.ingredient('garlic clove', 1, 'finely chopped')
    r.ingredient('green beans', Pound(1.5), 'tipped and cut into 2-inch lengths')
    r.ingredient('large ripe tomato', 1, 'peeled, seeded, and diced')
    r.ingredient('parsley', Teaspoon(2), 'chopped')
    r.ingredient('summer savory', Teaspoon(2))
    r.ingredient('dill', Teaspoon(2))
    r.ingredient('lovage', Teaspoon(2))
    r.ingredient('salt and pepper', None, 'to taste')

    # un-comment as desired
    r.doubleRecipe()
    # r.tripleRecipe()
    # r,quadroupleRecipe()

    # In general, make one call to instructions() per paragraph.
    r.instructions('Heat the oil in a medium or large skillet, add the onions and carrots, and cook over medium heat until soft and translucent, about 4 minutes.')

    r.instructions('Add the garlic, beans, tomato, and enough water just to cover. Simmer until the beans are tender, then add the herbs and simmer 1 or 2 minutes more. Timing will depend on the age and size of the bean. Season with salt and peper to taste.')
    
    r.instructions('Serve hot, tepid, or even chilled.')

    # r.yieldPerBatch(10, 'crepes')
    r.yieldPerBatch(4, 'large servings')

    # r.generate('crepes.pdf')
    return r.generate('greenBeansSimmeredWithTomato.pdf')

if __name__ == '__main__':
    generate()
