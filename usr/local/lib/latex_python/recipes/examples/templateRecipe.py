#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe, Ingredient
from latex_python.recipes.Quantities import Quart, Cup, Tablespoon, Teaspoon, FluidOunce, Bunch, Pound, Ounce


# title of the dish
recipe = Recipe('')

recipe.set(description='',  # Description shows up near the title.
           ingredients=[Ingredient('', 1, ''),
                        Ingredient('', 1, ''),
                        ],  # etc
           instructions=['paragraph 1',
                         'paragraph 2',
                         ]  # etc
           )

# ingredient name, quantity, prep/notes
# NOTE: Quantities can have a descriptive modifier like 'large' or 'overflowing'.
#       (there is no restriction on what can be identified)
# EX:   recipe.ingredient('brown rice', Cup(1.5, 'overflowing'))
#       recipe.ingredient('kale', Bunch(1, 'large'), 'chopped')
recipe.ingredient('', 1, '')

# un-comment as desired
# recipe.doubleRecipe()
# recipe.tripleRecipe()
# recipe.quadroupleRecipe()

# recipe.yieldPerBatch(10, 'crepes')
recipe.yieldPerBatch(FluidOunce(80))

if __name__ == '__main__':
    generate()
