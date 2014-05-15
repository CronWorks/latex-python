#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe
from latex_python.recipes.Quantities import Cup, FluidOunce, Tablespoon, Teaspoon, Bunch


def generate():
    # title of the dish
    r = Recipe('')

    # Description shows up near the title.
    r.description('''
    ''')

    # ingredient name, quantity, prep/notes
    # NOTE: Quantities can have a descriptive modifier like 'large' or 'overflowing'.
    #       (there is no restriction on what can be identified)
    # EX:   r.ingredient('brown rice', Cup(1.5, 'overflowing'))
    #       r.ingredient('kale', Bunch(1, 'large'), 'chopped')
    r.ingredient('', 1, '')

    # un-comment as desired
    # r.doubleRecipe()
    # r.tripleRecipe()
    # r,quadroupleRecipe()

    # In general, make one call to instructions() per paragraph.
    r.instructions('''
    ## paragraph 1 ##
    ''')

    r.instructions('''
    ## paragraph 2 ##
    ''')

    # r.yieldPerBatch(10, 'crepes')
    r.yieldPerBatch(FluidOunce(80))

    # r.generate('crepes.pdf')
    return r.generate()

if __name__ == '__main__':
    generate()
