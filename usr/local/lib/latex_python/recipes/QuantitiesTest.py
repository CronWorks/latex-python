'''
Created on May 10, 2014

@author: luke
'''
import unittest

from Quantities import Cup, Quart
from fractions import Fraction

class Test(unittest.TestCase):

    def testCups(self):
        c = Cup(1)
        self.assertEqual(str(c), '1c')
        self.assertEqual(c.fullString(), '1 cup')

        c = Cup(.5)
        self.assertEqual(str(c), '1/2c')
        self.assertEqual(c.fullString(), '1/2 cup')

        c = Cup('2/3')
        self.assertEqual(str(c), '2/3c')
        self.assertEqual(c.fullString(), '2/3 cup')

        c = Cup('1 1/2')
        self.assertEqual(c.quantity, 1.5)
        self.assertEqual(str(c), '1 1/2c')
        self.assertEqual(c.fullString(), '1 1/2 cups')

        c = Cup(8)  # 1 quart
        q = c.resolveQuantity()
        self.assertEqual(len(q), 1)
        self.assertIsInstance(q[0], Quart)
        self.assertEqual(q[0].quantity, 1)
        self.assertEqual(str(c), '1qt')
        self.assertEqual(c.fullString(), '1 quart')

        c = Cup(13)  # 1 5/8 quart (1qt + 5c)
        q = c.resolveQuantity()
        self.assertEqual(len(q), 2)
        self.assertIsInstance(q[0], Quart)
        self.assertIsInstance(q[1], Cup)
        self.assertEqual(q[0].quantity, 1)
        self.assertEqual(q[1].quantity, 5)
        self.assertEqual(str(c), '1qt + 5c')
        self.assertEqual(c.fullString(), '1 quart and 5 cups')

    def testQuarts(self):
        q = Quart(1)
        self.assertEqual(str(q), '1qt')
        self.assertEqual(q.fullString(), '1 quart')

        q = Quart(5)
        self.assertEqual(str(q), '5qt')
        self.assertEqual(q.fullString(), '5 quarts')

        q = Quart('2/3')
        self.assertEqual(str(q), '2/3qt')
        self.assertEqual(q.fullString(), '2/3 quart')

        q = Quart('1 1/2')
        self.assertEqual(q.quantity, 1.5)
        self.assertEqual(str(q), '1 1/2qt')
        self.assertEqual(q.fullString(), '1 1/2 quarts')

        q = Quart(13)
        q = q.resolveQuantity()  # should stay the same
        self.assertIsInstance(q[0], Quart)
        self.assertEqual(q[0].quantity, 13)
        self.assertEqual(str(q[0]), '13qt')
        self.assertEqual(q[0].fullString(), '13 quarts')


if __name__ == "__main__":
    # import sys;sys.argv = ['', 'Test.testQuantity']
    unittest.main()
