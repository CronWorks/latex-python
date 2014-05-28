#!/usr/bin/env python
# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe, Ingredient
from latex_python.recipes.Quantities import Quart, Cup, Tablespoon, Teaspoon, FluidOunce, Bunch, Pound, Ounce

recipe = Recipe('Whole Wheat Zucchini Banana Chocolate Chip Muffins')
recipe.set( ingredients=[Ingredient('whole wheat pastry flour', Cup(4, smartScaling=False)),
                         Ingredient('baking soda', Teaspoon(2)),
                         Ingredient('salt', Teaspoon(0.5)),
                         Ingredient('cinnamon', Teaspoon(0.5)),
                         Ingredient('large eggs', 2),
                         Ingredient('brown sugar', Cup('2/3'), 'packed'),
                         Ingredient('low-fat milk', Cup('2/3')),
                         Ingredient('vanilla extract', Teaspoon(3)),
                         Ingredient('unsalted butter', Cup(0.5), 'melted and cooled'),
                         Ingredient('zucchini', Cup('2 2/3'), 'freshly grated'),
                         Ingredient('mashed banana', Cup('2/3'), '1 large banana per cup'),
                         Ingredient('mini chocolate chips', Cup(1)),
                         ],
            instructions=['''Preheat oven to 350 degrees F. 
                             In a bowl, whisk together flour, baking soda, salt and cinnamon. 
                             Set aside. Line a muffin tin with liners.''',
                          '''In a large bowl, whisk egg and brown sugar together until smooth and no lumps remain. 
                             Add in vanilla extract, butter and milk, whisking again until smooth, 
                             then stir in zucchini and mashed bananas. 
                             Gradually add in dry ingredients, mixing until just combined. 
                             Fold in chocolate chips. Fill each muffin liner 2/3 of the way full with batter 
                             (I use a 1/4 cup measure to get the muffins to be of equal size).''',
                          '''Bake for 15-17 minutes, or until tops are no longer wet and become slightly golden. 
                             Remove and let cool until comfortable to the touch. 
                             Top with brown butter glaze if desired.''',
                          ]
            )

recipe.doubleRecipe()
recipe.yieldPerBatch(24, 'muffins')

if __name__ == '__main__':
    generate()

