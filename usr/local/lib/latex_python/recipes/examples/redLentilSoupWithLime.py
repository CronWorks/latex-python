# -*- coding: utf-8 -*-

from latex_python.recipes.Recipe import Recipe
from latex_python.recipes.Quantities import Cup, FluidOunce, Tablespoon, Teaspoon, Bunch


def generate():
    r = Recipe('Red Lentil Soup with Lime')

    r.doubleRecipe()
    r.tripleRecipe()

    r.ingredient('split red lentils', Cup(2), 'picked over and rinsed well')
    r.ingredient('turmeric', Tablespoon(1))
    r.ingredient('butter', Tablespoon(4))
    r.ingredient('salt', notes='to taste')

    r.ingredientGroup()
    r.ingredient('large onion', 1, 'finely diced (about 2 cups each)')
    r.ingredient('ground cumin', Teaspoon(2))
    r.ingredient('mustard seeds', Teaspoon(1.5), 'or 1 teaspoon ground mustard')

    r.ingredientGroup()
    r.ingredient('chopped cilantro', Bunch(1), 'about 1 cup per bunch')
    r.ingredient('juice of limes', 3, 'or to taste')
    r.ingredient('spinach', Bunch(1, 'large'), 'chopped into small pieces')
    r.ingredient('cooked rice', Cup(1))
    r.ingredient('yogurt', Tablespoon((4, 6)))


    r.description('''
    Easy, fast, and so very good! Althought the flavor is big, the soup is thin.
    Keep it brothy or include a spoonful of rice in each bowl for texture and body.
    A saffron-flavored rice is especially complementary.
    Torn pita bread briefly sautéed in olive oil until crisp is another very good addition to this soup.
    ''')

    r.instructions('''
    Put the lentils in a soup pot with 2 1/2 quarts water, the turmeric,
    1 tablespoon of the butter, and 1 tablespoon salt. Bring to a boil, then lower the heat and simmer, covered,
    until the lentils are soft and falling apart, about 20 minutes. Puree for a smooth and nicer-looking soup.
    ''')

    r.instructions('''
    While the soup is cooking, prepare the onion flavoring: In a medium skillet over low heat,
    cook the onion in 2 tablespoons of the remaining butter with the cumin and mustard, stirring occasionally.
    When soft, about the time the lentils are cooked or after 15 minutes, add the cilantro and cook for a minute more.
    Add the onion mixture to the soup, then add the juice of 2 limes.
    Taste, then add more if needed to bring up the flavors. The soup should be a tad sour.
    ''')

    r.instructions('''
    Just before serving, add the last tablespoon of butter to a wide skillet. When foamy, add the spinach,
    sprinkle with salt, and cook just long enough to wilt. If the rice is warm, place a spoonful in each bowl.
    If it's leftover rice, add it to the soup and let it heat through for a minute. Serve the soup, divide
    the spinach among the bowls, and swirl in a spoonful of yogurt.
    ''')

    r.yieldPerBatch(FluidOunce(80))

    return r.generate('redLentilSoupWithLime.pdf')

if __name__ == '__main__':
    generate()
