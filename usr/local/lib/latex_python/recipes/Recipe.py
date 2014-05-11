# /usr/bin/env python

from latex_python.JinjaBase import JinjaTexDocument
from py_base.PySystem import PySystem
from py_base.JobOutput import JobOutput
from Quantities import Quantity

from os.path import dirname, realpath
from fractions import Fraction
import re

# None is to ignore the [0] index
BATCH_NAMES = [None, 'Single', 'Double', 'Triple', 'Quadrouple']

class Recipe(JinjaTexDocument):

    def __init__(self, title, templateModule=None, searchPath=None):
        super(Recipe, self).__init__(templateModule, searchPath or realpath(dirname(__file__)))

        self.title = title

        # brief introductory paragraph about the recipe. Should be relatively brief,
        # should cover things like history, season, common pairings, etc.
        # free-form LaTeX (will not be escaped)
        self.descriptionText = ''

        # use addIngredient()
        self.ingredients = []

        # free-form LaTeX (will not be escaped)
        self.instructionsList = []

        # use Quantity or string to set this (string won't be auto-scaled)
        self.makes = {'amount': None,
                      'description': None}

        # misc
        self.fullQuantityText = False
        self.batches = set([1])
        self.commentsText = ''

    def description(self, description):
        self.descriptionText = description

    def instructions(self, instructions):
        self.instructionsList.append(instructions)

    def getDescriptionText(self):
        return self.generateTexFractions(self.descriptionText)

    def getInstructionsText(self):
        result = []
        for i in self.instructionsList:
            result.append(self.generateTexFractions(i))
        return ' \n\n'.join(result)

    def generateTexFractions(self, text):
        # replace two-part fractions (like '... 1 1/2 ...') WITHOUT a space
        text = re.sub(r'(\d)(\s)(\d)/(\d)([^\d])', r'\1$\\frac{\3}{\4}$\5', ' %s ' % text, flags=re.M)

        # replace any remaining one-part fractions (like '... 1/2 ...'), RETAINING the space
        text = re.sub(r'([^\d])(\d)/(\d)([^\d])', r'\1$\\frac{\2}{\3}$\4', ' %s ' % text, flags=re.M)

        return text.strip()

    def yieldPerBatch(self, amount, description=None):
        if isinstance(amount, str):
            if description == None:
                # it's just a description with no scalar value
                description = amount
                amount = None
            else:
                # try to convert str > Fraction
                amount = Fraction(amount)
        self.makes = {'amount': amount,
                      'description': description}

    def useFullQuantityText(self):
        self.fullQuantityText = True

    def doubleRecipe(self):
        self.batches.add(2)

    def tripleRecipe(self):
        self.batches.add(3)

    def quadroupleRecipe(self):
        self.batches.add(4)

    # use quantity == None for things like salt (i.e. to taste)
    def ingredient(self, name, quantity=None, notes=''):
        ingredient = {
            'name': name,
            'quantity': quantity,
            'notes': notes
        }
        self.ingredients.append(ingredient)

    def getIngredientsTable(self):
        columnSpec = ['l']
        headings = ['Item']
        for b in sorted(self.batches):
            columnSpec.append('l')
            # 'Single Batch', 'Double Batch', etc.
            if len(self.batches) == 1 and b == 1:
                # if we're only doing a single batch, don't mention batches.
                headings.append('Quantity')
            else:
                headings.append('%s Batch' % BATCH_NAMES[b])
        columnSpec.append('l')
        headings.append('Preparation/Notes')

        rows = []
        for ingredient in self.ingredients:
            columns = [ingredient['name']]
            for batch in sorted(self.batches):
                if ingredient['quantity'] is None:
                    columns.append('')
                else:
                    # ingredient.quantity will be either int, float, or Quantity
                    q = ingredient['quantity'] * batch
                    columns.append(self.quantityString(q))
            columns.append(ingredient['notes'])
            rows.append(' & '.join(columns))

        headingString = ' & '.join(['\\textbf{%s}' % h for h in headings])
        result = '''
            \\begin{tabular}{%s}
                %s \\\\
                \\hline
                %s
            \\end{tabular}
        ''' % (' '.join(columnSpec),
               headingString,
               ' \\\\\n'.join(rows))
        return result

    def quantityString(self, q, forceFullQuantityText=False):
        if isinstance(q, Quantity) and (forceFullQuantityText or self.fullQuantityText):
            result = self.generateTexFractions(q.fullString())
        else:
            result = self.generateTexFractions(str(q))
        return result

    def getYieldDescription(self):
        amount = self.makes['amount']
        description = self.makes['description']

        if amount:
            # we have a scalar amount so we can make an intelligent table of yields
            yields = []
            for b in sorted(self.batches):
                yields.append(('\\textbf{%s Batch:} %s %s' % (BATCH_NAMES[b],
                                                              self.quantityString(amount * b, True),
                                                              description or '')).strip())
            result = ' \\\\\n'.join(yields)
        else:
            result = 'Makes %s per batch' % description
        return result

    def generate(self, filename=None, system=None, variables={}):
        variables['recipe'] = self

        if not system:
            out = JobOutput()
            out.setVerbose()
            system = PySystem(out)
        if not filename:
            filename = self.title.replace(' ', '') + '.pdf'
        filename = realpath(filename)

        super(Recipe, self).generate(filename, system, variables)

