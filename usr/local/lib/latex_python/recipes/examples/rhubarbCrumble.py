#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe
from latex_python.recipes.Quantities import Quart, Cup, Tablespoon, Teaspoon, FluidOunce, Bunch, Pound, Ounce


def generate():
    # title of the dish
    r = Recipe('Rhubarb Crumble')

    # Description shows up near the title.
    r.description('Rhubarb offers a tart flavor that makes it a favorite ingredient in many springtime desserts. In this easy recipe, the greenish red stalks create a vibrant color and a fruity tart flavor. You can use white all-purpose flour or whole-wheat pastry flour or swap the flour with quick oats to make the dish more nutritious. The crumble can be eaten alone or smothered in ice cream!')

    # ingredient name, quantity, prep/notes
    # NOTE: Quantities can have a descriptive modifier like 'large' or 'overflowing'.
    #       (there is no restriction on what can be identified)
    # EX:   r.ingredient('brown rice', Cup(1.5, 'overflowing'))
    #       r.ingredient('kale', Bunch(1, 'large'), 'chopped')
    r.ingredient('fresh rhubarb', Pound(1), '')
    r.ingredient('sugar', Cup(0.75), '')
    r.ingredient('unsalted butter', Tablespoon(6), '')
    r.ingredient('flour', Cup(0.75), '')
    r.ingredient('raw or brown sugar', Tablespoon(1), 'for topping')

    # un-comment as desired
    r.doubleRecipe()
    # r.tripleRecipe()
    # r,quadroupleRecipe()

    # In general, make one call to instructions() per paragraph.
    r.instructions('Heat oven to 350 degrees F.')
    r.instructions('Cut rhubarb into chunks, place it in a 9"x9" oven-safe dish, and cover with 1/3 of the sugar.')
    r.instructions('In a separate bowl, cut in butter into the flour until the mixture resembles bread crumbs, and then add remaining portion of sugar.')
    r.instructions('Sprinkle the flour/butter/sugar mixture on top of the rhubarb.')
    r.instructions('Place in oven and bake for 40-45 minutes. Then remove from oven and let cool.')
    r.instructions('Top with the raw or brown sugar just before serving. ')

    # r.yieldPerBatch(10, 'crepes')
    r.yieldPerBatch(Cup(4.5))

    # r.generate('crepes.pdf')
    return r.generate('RhubarbCrumble.pdf')

if __name__ == '__main__':
    generate()

